import mlflow
from mlflow.types.llm import (ChatMessage,ChatParams,ChatCompletionResponse,FunctionToolDefinition, ToolDefinition,ToolParamsSchema,ParamProperty)
from openai import OpenAI
from mlflow.models import set_model
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

        print(self.tools)
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=self.tools,
        )

        tool_calls = response.choices[0].message.tool_calls
        messages.append(response.choices[0].message)
        if tool_calls:
            for tool_call in tool_calls:
                tool_response = ChatMessage(
                    role="tool",
                    content=locals()["tool_call.function.name"](
                        **tool_call.function.arguments
                    ),
                    tool_call_id=tool_call.id,
                ).to_dict()

                messages.append(tool_response)
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            # tools=self.tools,
        )

        return ChatCompletionResponse.from_dict(response.to_dict())

        def get_random_joke(self):
            """
            This function retrieves a random joke from the Official Joke API.

            Returns:
            dict: A dictionary containing the random joke.
            """
            url = "https://official-joke-api.appspot.com/random_joke"
            response = requests.get(url)
            return response.json()

        def get_joke_types(self):
            """
            This function retrieves the available joke types from the Official Joke API.

            Returns:
            list: A list of available joke types.
            """
            url = "https://official-joke-api.appspot.com/types"
            response = requests.get(url)
            return response.json()

        def get_multiple_random_jokes(self, num_jokes):
            """
            This function retrieves the specified number of random jokes from the Official Joke API.

            Parameters:
            num_jokes (int): The number of random jokes to retrieve.

            Returns:
            list: A list of random jokes.
            """
            url = f"https://official-joke-api.appspot.com/jokes/random/{num_jokes}"
            response = requests.get(url)
            return response.json()

        def get_jokes_by_type(self, joke_type, num_jokes=1):
            """
            This function retrieves the specified number of jokes of the given type from the Official Joke API.

            Parameters:
            joke_type (str): The type of joke to retrieve.
            num_jokes (int): The number of jokes to retrieve (default is 1).

            Returns:
            list: A list of jokes of the specified type.
            """
            if num_jokes == 1:
                url = f"https://official-joke-api.appspot.com/jokes/{joke_type}/random"
            else:
                url = f"https://official-joke-api.appspot.com/jokes/{joke_type}/ten"
            response = requests.get(url)
            return response.json()

        def get_joke_by_id(self, joke_id):
            """
            This function retrieves a joke by its ID from the Official Joke API.

            Parameters:
            joke_id (int): The ID of the joke to retrieve.

            Returns:
            dict: A dictionary containing the joke.
            """
            url = f"https://official-joke-api.appspot.com/jokes/{joke_id}"
            response = requests.get(url)
            return response.json()

set_model(NewAgent([{'function': {'name': 'get_random_joke', 'description': 'This function retrieves a random joke from the Official Joke API.\n    \n    Returns:\n    dict: A dictionary containing the random joke.', 'parameters': {'properties': {}, 'type': 'object'}, 'strict': False}, 'type': 'function'}, {'function': {'name': 'get_joke_types', 'description': 'This function retrieves the available joke types from the Official Joke API.\n    \n    Returns:\n    list: A list of available joke types.', 'parameters': {'properties': {}, 'type': 'object'}, 'strict': False}, 'type': 'function'}, {'function': {'name': 'get_multiple_random_jokes', 'description': 'This function retrieves the specified number of random jokes from the Official Joke API.\n    \n    ', 'parameters': {'properties': {'num_jokes': {'type': 'integer', 'description': 'The number of random jokes to retrieve.'}}, 'type': 'object'}, 'strict': False}, 'type': 'function'}, {'function': {'name': 'get_jokes_by_type', 'description': 'This function retrieves the specified number of jokes of the given type from the Official Joke API.\n    \n    ', 'parameters': {'properties': {'joke_type': {'type': 'string', 'description': 'The type of joke to retrieve.'}, 'num_jokes': {'type': 'integer', 'description': 'The number of jokes to retrieve (default is 1).'}}, 'type': 'object'}, 'strict': False}, 'type': 'function'}, {'function': {'name': 'get_joke_by_id', 'description': 'This function retrieves a joke by its ID from the Official Joke API.\n    \n    ', 'parameters': {'properties': {'joke_id': {'type': 'integer', 'description': 'The ID of the joke to retrieve.'}}, 'type': 'object'}, 'strict': False}, 'type': 'function'}], ['get_random_joke', 'get_joke_types', 'get_multiple_random_jokes', 'get_jokes_by_type', 'get_joke_by_id']))