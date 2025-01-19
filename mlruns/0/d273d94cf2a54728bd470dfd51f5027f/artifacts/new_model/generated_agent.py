import mlflow
from mlflow.types.llm import (ChatMessage,ChatParams,ChatCompletionResponse,FunctionToolDefinition, ToolDefinition,ToolParamsSchema,ParamProperty)
from openai import OpenAI
from mlflow.models import set_model; import json
import requests
MODEL = "mixtral-8x7b-32768"


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

    def get_random_joke(self):
        """
        This function returns a random joke.

        Returns:
        dict: A dictionary containing the joke data.
        """
        url = "https://official-joke-api.appspot.com/random_joke"
        response = requests.get(url)
        data = response.json()
        return data

    def get_joke_types(self):
        """
        This function returns a list of joke types.

        Returns:
        list: A list of joke types.
        """
        url = "https://official-joke-api.appspot.com/types"
        response = requests.get(url)
        data = response.json()
        return data

    def get_multiple_random_jokes(self, num_jokes):
        """
        This function returns a specified number of random jokes.

        Parameters:
        num_jokes (int): The number of jokes to retrieve.

        Returns:
        list: A list of joke data.
        """
        url = f"https://official-joke-api.appspot.com/jokes/random/{num_jokes}"
        response = requests.get(url)
        data = response.json()
        return data

    def get_jokes_by_type(self, joke_type, num_jokes=1):
        """
        This function returns a specified number of jokes of a specific type.

        Parameters:
        joke_type (str): The type of joke to retrieve.
        num_jokes (int): The number of jokes to retrieve. Default is 1.

        Returns:
        list: A list of joke data.
        """
        if num_jokes == 1:
            url = f"https://official-joke-api.appspot.com/jokes/{joke_type}/random"
        else:
            url = f"https://official-joke-api.appspot.com/jokes/{joke_type}/ten"
        response = requests.get(url)
        data = response.json()
        return data

    def get_joke_by_id(self, joke_id):
        """
        This function returns a joke by its ID.

        Parameters:
        joke_id (int): The ID of the joke to retrieve.

        Returns:
        dict: A dictionary containing the joke data.
        """
        url = f"https://official-joke-api.appspot.com/jokes/{joke_id}"
        response = requests.get(url)
        data = response.json()
        return data

set_model(NewAgent([{'function': {'name': 'get_random_joke', 'description': 'This function returns a random joke.\n    \n    Returns:\n    dict: A dictionary containing the joke data.', 'parameters': {'properties': {}, 'type': 'object'}, 'strict': True}, 'type': 'function'}, {'function': {'name': 'get_joke_types', 'description': 'This function returns a list of joke types.\n    \n    Returns:\n    list: A list of joke types.', 'parameters': {'properties': {}, 'type': 'object'}, 'strict': True}, 'type': 'function'}, {'function': {'name': 'get_multiple_random_jokes', 'description': 'This function returns a specified number of random jokes.\n    \n    ', 'parameters': {'properties': {'num_jokes': {'type': 'integer', 'description': 'The number of jokes to retrieve.'}}, 'type': 'object'}, 'strict': True}, 'type': 'function'}, {'function': {'name': 'get_jokes_by_type', 'description': 'This function returns a specified number of jokes of a specific type.\n    \n    ', 'parameters': {'properties': {'joke_type': {'type': 'string', 'description': 'The type of joke to retrieve.'}, 'num_jokes': {'type': 'integer', 'description': 'The number of jokes to retrieve. Default is 1.'}}, 'type': 'object'}, 'strict': True}, 'type': 'function'}, {'function': {'name': 'get_joke_by_id', 'description': 'This function returns a joke by its ID.\n    \n    ', 'parameters': {'properties': {'joke_id': {'type': 'integer', 'description': 'The ID of the joke to retrieve.'}}, 'type': 'object'}, 'strict': True}, 'type': 'function'}], ['get_random_joke', 'get_joke_types', 'get_multiple_random_jokes', 'get_jokes_by_type', 'get_joke_by_id']))