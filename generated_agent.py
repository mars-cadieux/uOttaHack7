import mlflow
from mlflow.types.llm import (ChatMessage, ChatParams, ChatCompletionResponse)
from mlflow.entities.span import SpanType
from openai import OpenAI
from mlflow.models import set_model
import json
import requests
import json

tools = [{"function": {"name": "get_pokemon_info", "description": "This function takes a Pok\u00e9mon ID as input and returns the Pok\u00e9mon information.\n    \n    ", "parameters": {"properties": {"pokemon_id": {"type": "integer", "description": "The ID of the Pok\u00e9mon."}}, "type": "object"}, "strict": True}, "type": "function"}, {"function": {"name": "get_pokemon_species_info", "description": "This function takes a Pok\u00e9mon species ID as input and returns the Pok\u00e9mon species information.\n    \n    ", "parameters": {"properties": {"pokemon_species_id": {"type": "integer", "description": "The ID of the Pok\u00e9mon species."}}, "type": "object"}, "strict": True}, "type": "function"}, {"function": {"name": "get_pokemon_types", "description": "This function takes a Pok\u00e9mon ID as input and returns the Pok\u00e9mon types.\n    \n    ", "parameters": {"properties": {"pokemon_id": {"type": "integer", "description": "The ID of the Pok\u00e9mon."}}, "type": "object"}, "strict": True}, "type": "function"}]
functions = ["get_pokemon_info", "get_pokemon_species_info", "get_pokemon_types"]
MODEL = "llama3-8b-8192"


class NewAgent(mlflow.pyfunc.ChatModel):
    def __init__(self):
        self.tools = tools
        self.functions = functions

    def predict(self, context, messages: list[ChatMessage], params: ChatParams):
        client = OpenAI(
            api_key="YOUR_KEY_HERE",
            base_url="https://api.groq.com/openai/v1",
        )

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
                if args is None or "none" in args or "" in args or "properties" in args:
                    content = method()
                else:
                    content = method(**args)
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

    @mlflow.trace(span_type=SpanType.TOOL)
    def get_pokemon_info(self, pokemon_id):
        """
        This function takes a Pokémon ID as input and returns the Pokémon information.

        Parameters:
        pokemon_id (int): The ID of the Pokémon.

        Returns:
        dict: A dictionary containing the Pokémon information.
        """
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
        response = requests.get(url)
        data = json.loads(response.text)
        return data

    @mlflow.trace(span_type=SpanType.TOOL)
    def get_pokemon_species_info(self, pokemon_species_id):
        """
        This function takes a Pokémon species ID as input and returns the Pokémon species information.

        Parameters:
        pokemon_species_id (int): The ID of the Pokémon species.

        Returns:
        dict: A dictionary containing the Pokémon species information.
        """
        url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_species_id}/"
        response = requests.get(url)
        data = json.loads(response.text)
        return data

    @mlflow.trace(span_type=SpanType.TOOL)
    def get_pokemon_types(self, pokemon_id):
        """
        This function takes a Pokémon ID as input and returns the Pokémon types.

        Parameters:
        pokemon_id (int): The ID of the Pokémon.

        Returns:
        dict: A dictionary containing the Pokémon types.
        """
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/types/"
        response = requests.get(url)
        data = json.loads(response.text)
        return data

set_model(NewAgent())