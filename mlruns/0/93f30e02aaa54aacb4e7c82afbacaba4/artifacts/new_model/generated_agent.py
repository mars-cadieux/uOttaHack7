import mlflow
from mlflow.types.llm import (ChatMessage,ChatParams,ChatCompletionResponse,FunctionToolDefinition, ToolDefinition,ToolParamsSchema,ParamProperty)
from openai import OpenAI
from mlflow.models import set_model; import json
import requests
import json
MODEL = "gemma2-9b-it"


class NewAgent(mlflow.pyfunc.ChatModel):
    def __init__(self, tools, functions):
        self.tools = tools
        self.functions = functions

    def predict(self, context, messages: list[ChatMessage], params: ChatParams):
        client = OpenAI(
            api_key="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",
            base_url="https://api.groq.com/openai/v1",
        )

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
                if tool_call.function.arguments is not dict:
                    tool_call.function.arguments = json.loads(
                        tool_call.function.arguments
                    )
                print(tool_call.function.arguments)
                if (
                    tool_call.function.arguments is None
                    or "none" in tool_call.function.arguments
                    or "" in tool_call.function.arguments
                    or "properties" in tool_call.function.arguments
                ):
                    content = method()
                else:
                    content = method(**tool_call.function.arguments)
                tool_response = ChatMessage(
                    role="tool", content=str(content), tool_call_id=tool_call.id
                ).to_dict()
                print(tool_response["content"])
                response = {}
                response["content"] = tool_response["content"]
                response["choices"] = [{"message": {}}]
                response["choices"][0]["message"]["content"] = tool_response["content"]
                response["choices"][0]["message"]["role"] = "assistant"
        # response = client.chat.completions.create(
        #     model=MODEL,
        #     messages=messages,
        #     tools=self.tools,
        # )

        return ChatCompletionResponse.from_dict(response)

    def get_random_fact(self):
        """
        This function returns a random cat fact.

        Returns:
        dict: A dictionary containing a random cat fact.
        """
        url = "https://catfact.ninja/fact"
        response = requests.get(url)
        data = json.loads(response.text)
        return data

    def get_multiple_facts(self, limit):
        """
        This function takes the number of facts as input and returns multiple random cat facts.

        Parameters:
        limit (int): The number of facts to return.

        Returns:
        list: A list of dictionaries containing multiple random cat facts.
        """
        url = f"https://catfact.ninja/facts?limit={limit}"
        response = requests.get(url)
        data = json.loads(response.text)
        return data["data"]

    def install_catfact_library(self):
        """
        This function installs the catfact library using pip.

        Returns:
        None
        """
        import subprocess

        subprocess.run(["pip", "install", "catfact"])

set_model(NewAgent([{'function': {'name': 'get_random_fact', 'description': 'This function returns a random cat fact.\n    \n    Returns:\n    dict: A dictionary containing a random cat fact.', 'parameters': {'properties': {}, 'type': 'object'}, 'strict': True}, 'type': 'function'}, {'function': {'name': 'get_multiple_facts', 'description': 'This function takes the number of facts as input and returns multiple random cat facts.\n    \n    ', 'parameters': {'properties': {'limit': {'type': 'integer', 'description': 'The number of facts to return.'}}, 'type': 'object'}, 'strict': True}, 'type': 'function'}, {'function': {'name': 'install_catfact_library', 'description': 'This function installs the catfact library using pip.\n    \n    Returns:\n    None', 'parameters': {'properties': {}, 'type': 'object'}, 'strict': True}, 'type': 'function'}], ['get_random_fact', 'get_multiple_facts', 'install_catfact_library']))