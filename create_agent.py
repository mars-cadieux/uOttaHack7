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

def fix_python_indentation(python_string):
    try:
        reformatted_code = black.format_str(python_string, mode=Mode())
        return reformatted_code
    except black.NothingChanged:
        return python_string  # Code is already correctly formatted
    except Exception as e:
        raise ValueError(f"Error formatting code: {e}")
    


nest_asyncio.apply()

agent_class = """\n\n
MODEL = "gemma2-9b-it"

class NewAgent(mlflow.pyfunc.ChatModel):
    def __init__(self, tools, functions):
        self.tools = tools
        self.functions = functions

    def predict(self, context, messages: list[ChatMessage], params: ChatParams):
        client = OpenAI(api_key="",
                        base_url="https://api.groq.com/openai/v1")

        messages = [m.to_dict() for m in messages]

        print(messages)
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=self.tools,
        )

        tool_calls = response.choices[0].message.tool_calls
        messages.append(response.choices[0].message)
        if tool_calls:
            for tool_call in tool_calls:
                method = getattr(self, tool_call.function.name, None)
                if(tool_call.function.arguments is not dict):
                    tool_call.function.arguments = json.loads(tool_call.function.arguments)
                print(tool_call.function.arguments)
                if(tool_call.function.arguments is None or 'none' in tool_call.function.arguments or '' in tool_call.function.arguments or 'properties' in tool_call.function.arguments):
                    content=method()
                else:
                    content=method(**tool_call.function.arguments)
                tool_response = ChatMessage(
                    role="tool", content=str(content), tool_call_id=tool_call.id
                ).to_dict()
                # print(tool_response['content'])
                # response = {}
                # response['content'] = tool_response['content']
                # response['choices'] = [{'message':{}}]
                # response['choices'][0]['message']['content'] = tool_response['content']
                # response['choices'][0]['message']['role'] = "assistant"
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=self.tools,
        )

        return ChatCompletionResponse.from_dict(response)

"""


async def main():
    modelResponse = await createPythonTools("https://catfact.ninja/docs/api-docs.json")
    libList, functionsList = parseModelTools(modelResponse)
    type_conversion = {'str': 'string', 'float': 'number', 'int': 'integer', 
                       'obj': 'object', 'arr': 'array', 'bool': 'boolean'}
    tools = []
    functions = []
    for obj in functionsList:
        functions.append(obj['function_name'])
        params_obj = obj['description']
        param_schema_obj = {}
        if "Parameters:" in params_obj:
            desc, param_str = params_obj.split("Parameters:")
            lines = param_str.split('\n')
            for line in lines:
                print(line)
                if(len(line.strip().split(' ')) <= 2):
                    continue
                word, rest = line.strip().split(' ', 1)
                keywords = ["Returns:", "list:", "dict:"]
                if(word not in keywords):
                    type, param_desc = rest.strip().split(' ', 1)
                    param_schema_obj[word] = ParamProperty(type=type_conversion[type[1:-2]], description=param_desc)
            new_tool = FunctionToolDefinition(name=obj['function_name'], description=desc, parameters=ToolParamsSchema(param_schema_obj),strict=True)
        else:
            new_tool = FunctionToolDefinition(name=obj['function_name'], description=obj['description'], parameters=ToolParamsSchema({}),strict=True)
        tools.append(new_tool.to_tool_definition().to_dict())
    _, rest = modelResponse.split("CODE:")
    import_segment, func_segment = rest.split("#$END$")
    func_segment = func_segment
    _, import_segment = import_segment.split("#$START$", 1)
    func_segment = '\t'+ func_segment
    func_segment = func_segment.replace("\n", "\n\t")
    func_segment = func_segment.replace("\t", "    ")
    combined_agent_class = agent_class + func_segment 
    class_imports = "import mlflow\nfrom mlflow.types.llm import (ChatMessage,ChatParams,ChatCompletionResponse,FunctionToolDefinition, ToolDefinition,ToolParamsSchema,ParamProperty)\n" + \
                    "from openai import OpenAI\nfrom mlflow.models import set_model; import json"
    pattern = r'(?m)^(\s*)def\s+([a-zA-Z_][a-zA-Z_0-9]*)\s*\((.*?)\):'
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
    combined_agent_class = re.sub(pattern, add_self_to_args, combined_agent_class)
    with open("generated_agent.py", "w") as f:
        f.write(class_imports+import_segment
                +fix_python_indentation(combined_agent_class)+f"\nset_model(NewAgent({tools}, {functions}))")
    system_prompt = {
        "role": "system",
        "content": "Please use the provided tools to answer user queries using the provided tools. Be sure to follow the correct syntax when generating tool calls and follow the schema for input when making function calls.",
    }
    messages = [
        system_prompt,
        {"role": "user", "content": "Give me a random cat fact"},
    ]
    input_example = {
        "messages": messages,
    }
    
    with mlflow.start_run():
        model_info = mlflow.pyfunc.log_model(
            artifact_path="new_model",
            python_model="generated_agent.py",
            input_example=input_example,
        )

        model_uri = model_info.model_uri
    # tool_model = mlflow.pyfunc.load_model(model_uri)


    # response = tool_model.predict({"messages": messages})
    # print(response["choices"][0]["message"]["content"])
    # os.system(f"export OPENAI_API_KEY=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")
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

