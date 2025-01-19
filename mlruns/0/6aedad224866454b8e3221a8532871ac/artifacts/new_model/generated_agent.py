import mlflow
from mlflow.types.llm import (ChatMessage,ChatParams,ChatCompletionResponse,FunctionToolDefinition, ToolDefinition,ToolParamsSchema,ParamProperty)
from openai import OpenAI
from mlflow.models import set_model; import json
import requests
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

    def get_random_cat_fact(self):
        """
        This function returns a single random cat fact.

        Returns:
        dict: A dictionary containing the random cat fact.
        """
        url = "https://catfact.ninja/fact"
        response = requests.get(url)
        return response.json()

    def get_multiple_random_cat_facts(self, limit=1):
        """
        This function returns multiple random cat facts.

        Parameters:
        limit (int): The number of facts to return. Defaults to 1, max is 500.

        Returns:
        dict: A dictionary containing the multiple random cat facts.
        """
        url = f"https://catfact.ninja/facts?limit={limit}"
        response = requests.get(url)
        return response.json()

    def get_cat_facts_with_limit(self, limit):
        """
        This function returns cat facts with a specified limit.

        Parameters:
        limit (int): The number of facts to return. Must be between 1 and 500.

        Returns:
        dict: A dictionary containing the cat facts with the specified limit.
        """
        if not 1 <= limit <= 500:
            raise ValueError("Limit must be between 1 and 500")
        url = f"https://catfact.ninja/facts?limit={limit}"
        response = requests.get(url)
        return response.json()

set_model(NewAgent([{'function': {'name': 'get_random_cat_fact', 'description': 'This function returns a single random cat fact.\n    \n    Returns:\n    dict: A dictionary containing the random cat fact.', 'parameters': {'properties': {}, 'type': 'object'}, 'strict': True}, 'type': 'function'}, {'function': {'name': 'get_multiple_random_cat_facts', 'description': 'This function returns multiple random cat facts.\n    \n    ', 'parameters': {'properties': {'limit': {'type': 'integer', 'description': 'The number of facts to return. Defaults to 1, max is 500.'}}, 'type': 'object'}, 'strict': True}, 'type': 'function'}, {'function': {'name': 'get_cat_facts_with_limit', 'description': 'This function returns cat facts with a specified limit.\n    \n    ', 'parameters': {'properties': {'limit': {'type': 'integer', 'description': 'The number of facts to return. Must be between 1 and 500.'}}, 'type': 'object'}, 'strict': True}, 'type': 'function'}], ['get_random_cat_fact', 'get_multiple_random_cat_facts', 'get_cat_facts_with_limit']))