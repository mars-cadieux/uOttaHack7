from parser import parseModelTools
from tool_retrieval import createPythonTools
import nest_asyncio
import asyncio
import os
import json
import re
from time import sleep
import requests
import mlflow
import requests
import json
from mlflow.types.llm import (
    FunctionToolDefinition,
    ParamProperty,
    ToolParamsSchema,
)
from mlflow.entities.span import (
    SpanType,
)

from mlflow.models import set_model
import black
from black.mode import Mode

from search import getSingleResult

userQuery = "pokemon"

def fix_python_indentation(python_string):
    try:
        reformatted_code = black.format_str(python_string, mode=Mode())
        return reformatted_code
    except black.NothingChanged:
        return python_string  # Code is already correctly formatted
    except Exception as e:
        raise ValueError(f"Error formatting code: {e}")
    
nest_asyncio.apply()

agent_class = """

MODEL = "llama-3.3-70b-versatile"

class NewAgent(mlflow.pyfunc.ChatModel):
    def __init__(self):
        self.tools = tools
        self.functions = functions

    def predict(self, context, messages: list[ChatMessage], params: ChatParams):
        client = OpenAI(api_key="YOUR_KEY_HERE",
                        base_url="https://api.groq.com/openai/v1")

        messages = [m.to_dict() for m in messages]

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=self.tools,
        )

        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            messages.append(response.choices[0].message)
            for tool_call in tool_calls:
                method = getattr(self, tool_call.function.name, None)
                args = json.loads(tool_call.function.arguments)
                if (
                    args is None
                    or "none" in args
                    or "" in args
                    or "properties" in args
                ):
                    content=method()
                else:
                    content=method(**args)
                tool_response = ChatMessage(
                    role="tool", content=str(content), tool_call_id=tool_call.id
                ).to_dict()
                messages.append(tool_response)
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=self.tools,
            )

        return ChatCompletionResponse.from_dict(response.to_dict())

"""


async def main():
    searchResult = getSingleResult(userQuery)
    modelResponse = await createPythonTools(searchResult)
    libList, functionsList = parseModelTools(modelResponse)
    func_def_pattern = r'(?m)^(\s*)def\s+([a-zA-Z_][a-zA-Z_0-9]*)\s*\((.*?)\):'
    type_conversion = {'str': 'string', 'float': 'number', 'int': 'integer', 
                       'obj': 'object', 'arr': 'array', 'bool': 'boolean', '': 'none'}
    tools = []
    functions = []
    for obj in functionsList:
        functions.append(obj['function_name'])
        params_obj = obj['description']
        param_schema_obj = {}
        if "Parameters:" in params_obj:
            desc, param_str = params_obj.split("Parameters:")
            if "Returns:" in param_str:
                param_str, _ = param_str.split("Returns:")
            lines = param_str.split('\n')
            for line in lines:
                if(len(line.strip().split(' ')) <= 2):
                    continue
                word, rest = line.strip().split(' ', 1)
                keywords = ["Returns:", "list:", "dict:"]
                if(word not in keywords):
                    type, param_desc = rest.strip().split(' ', 1)
                    type_str = type[1:-2]
                    type_str = type_conversion[type_str] if type_str in type_conversion else "object"
                    param_schema_obj[word] = ParamProperty(type=type_str, description=param_desc)
            new_tool = FunctionToolDefinition(name=obj['function_name'], description=desc, parameters=ToolParamsSchema(param_schema_obj), strict=True)
        else:
            new_tool = FunctionToolDefinition(name=obj['function_name'], description=obj['description'], parameters=ToolParamsSchema({}), strict=True)
        tools.append(new_tool.to_tool_definition().to_dict())
    
    _, rest = modelResponse.split("CODE:")
    import_segment, func_segment = rest.split("#$END$")
    func_segment = func_segment
    _, import_segment = import_segment.split("#$START$", 1)
    def add_line_before(match):
        indentation = match.group(1)
        return f"{indentation}@mlflow.trace(span_type=SpanType.TOOL)\n{match.group(0)}"
    func_segment = re.sub(func_def_pattern, add_line_before, func_segment)
    func_segment = '\t'+ func_segment
    func_segment = func_segment.replace("\n", "\n\t")
    func_segment = func_segment.replace("\t", "    ")
    combined_agent_class = agent_class + func_segment 
    class_imports = "import mlflow\nfrom mlflow.types.llm import (ChatMessage, ChatParams, ChatCompletionResponse)\nfrom mlflow.entities.span import SpanType\n" + \
                    "from openai import OpenAI\nfrom mlflow.models import set_model\nimport json"
    def add_self_to_args(match):
        indentation = match.group(1)  # Leading whitespace
        function_name = match.group(2)
        args = match.group(3).strip()

        if(function_name == "__init__" or function_name == "predict"):
            new_args = args
        else:
            if args:  # If there are existing arguments
                new_args = f"self, {args}"
            else:  # No arguments
                new_args = "self"

        return f"{indentation}def {function_name}({new_args}):"
    combined_agent_class = re.sub(func_def_pattern, add_self_to_args, combined_agent_class)
    tools_string = json.dumps(tools).replace("true", "True").replace("false", "False")
    functions_string = json.dumps(functions).replace("true", "True").replace("false", "False")
    with open("generated_agent.py", "w") as f:
        f.write(class_imports+import_segment+f"\ntools = {tools_string}\nfunctions = {functions_string}\n"
                +fix_python_indentation(combined_agent_class)+f"\nset_model(NewAgent())")
    # system_prompt = {
    #     "role": "system",
    #     "content": "Please use the provided tools to answer user queries.",
    # }
    # messages = [
    #     system_prompt,
    #     # {"role": "user", "content": "Tell me " + userQuery},
    #     {"role": "user", "content": "Tell me the weather in Ottawa right now"},
    # ]
    # input_example = {
    #     "messages": messages,
    # }
    
    # with mlflow.start_run():
    #     model_info = mlflow.pyfunc.log_model(
    #         artifact_path="new_model",
    #         python_model="generated_agent.py",
    #         input_example=input_example,
    #     )
    #     model_uri = model_info.model_uri
    # tool_model = mlflow.pyfunc.load_model(model_uri)


    # response = tool_model.predict({"messages": messages})
    # print(response["choices"][0]["message"]["content"])
    # os.system(f"export OPENAI_API_KEY=")
    # os.system(f"mlflow models serve -m {modeul_uri}")

    # sleep(5)
    # messages = [
    #     {"role": "user", "content": "Tell me a joke"},
    # ]

    # response = requests.post("http://127.0.0.1:5000/invocations", json={"messages": messages})
    # response.raise_for_status()
    # print(response.json())


if __name__ == "__main__":
    asyncio.run(main())

