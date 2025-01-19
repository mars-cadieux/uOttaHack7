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

    def get_random_joke(self):
        """
        This function returns a random joke.

        Returns:
        dict: A dictionary containing the random joke data.
        """
        url = "https://official-joke-api.appspot.com/random_joke"
        response = requests.get(url)
        data = response.json()
        return data

    def get_joke_types(self):
        """
        This function returns the available joke types.

        Returns:
        list: A list of joke types.
        """
        url = "https://official-joke-api.appspot.com/types"
        response = requests.get(url)
        data = response.json()
        return data

    def get_multiple_random_jokes(self, num_jokes):
        """
        This function takes the number of jokes as input and returns that many random jokes.

        Parameters:
        num_jokes (int): The number of jokes to retrieve.

        Returns:
        list: A list of dictionaries containing the random joke data.
        """
        url = f"https://official-joke-api.appspot.com/jokes/random/{num_jokes}"
        response = requests.get(url)
        data = response.json()
        return data

    def get_jokes_by_type(self, joke_type):
        """
        This function takes the joke type as input and returns jokes of that type.

        Parameters:
        joke_type (str): The type of jokes to retrieve.

        Returns:
        list: A list of dictionaries containing the joke data.
        """
        url = f"https://official-joke-api.appspot.com/jokes/{joke_type}/random"
        response = requests.get(url)
        data = response.json()
        return data

    def get_joke_by_id(self, joke_id):
        """
        This function takes the joke ID as input and returns the joke with that ID.

        Parameters:
        joke_id (int): The ID of the joke to retrieve.

        Returns:
        dict: A dictionary containing the joke data.
        """
        url = f"https://official-joke-api.appspot.com/jokes/{joke_id}"
        response = requests.get(url)
        data = response.json()
        return data

set_model(NewAgent([{'function': {'name': 'get_random_joke', 'description': 'This function returns a random joke.\n    \n    Returns:\n    dict: A dictionary containing the random joke data.', 'parameters': {'properties': {}, 'type': 'object'}, 'strict': True}, 'type': 'function'}, {'function': {'name': 'get_joke_types', 'description': 'This function returns the available joke types.\n    \n    Returns:\n    list: A list of joke types.', 'parameters': {'properties': {}, 'type': 'object'}, 'strict': True}, 'type': 'function'}, {'function': {'name': 'get_multiple_random_jokes', 'description': 'This function takes the number of jokes as input and returns that many random jokes.\n    \n    ', 'parameters': {'properties': {'num_jokes': {'type': 'integer', 'description': 'The number of jokes to retrieve.'}}, 'type': 'object'}, 'strict': True}, 'type': 'function'}, {'function': {'name': 'get_jokes_by_type', 'description': 'This function takes the joke type as input and returns jokes of that type.\n    \n    ', 'parameters': {'properties': {'joke_type': {'type': 'string', 'description': 'The type of jokes to retrieve.'}}, 'type': 'object'}, 'strict': True}, 'type': 'function'}, {'function': {'name': 'get_joke_by_id', 'description': 'This function takes the joke ID as input and returns the joke with that ID.\n    \n    ', 'parameters': {'properties': {'joke_id': {'type': 'integer', 'description': 'The ID of the joke to retrieve.'}}, 'type': 'object'}, 'strict': True}, 'type': 'function'}], ['get_random_joke', 'get_joke_types', 'get_multiple_random_jokes', 'get_jokes_by_type', 'get_joke_by_id']))