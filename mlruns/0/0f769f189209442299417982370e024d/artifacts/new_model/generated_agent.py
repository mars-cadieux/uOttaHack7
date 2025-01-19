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

    def get_current_weather(self, latitude, longitude):
        """
        This function takes the latitude and longitude of a location as input and returns the current weather.

        Parameters:
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.

        Returns:
        dict: A dictionary containing the current weather data.
        """
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        response = requests.get(url)
        data = json.loads(response.text)
        return data["current_weather"]

    def get_hourly_forecast(self, latitude, longitude):
        """
        This function takes the latitude and longitude of a location as input and returns the hourly forecast.

        Parameters:
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.

        Returns:
        dict: A dictionary containing the hourly forecast data.
        """
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
        response = requests.get(url)
        data = json.loads(response.text)
        return data["hourly"]

    def get_historical_weather(self, latitude, longitude, start_date, end_date):
        """
        This function takes the latitude, longitude, start date, and end date as input and returns the historical weather data.

        Parameters:
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.
        start_date (str): The start date for which to retrieve the historical weather data.
        end_date (str): The end date for which to retrieve the historical weather data.

        Returns:
        dict: A dictionary containing the historical weather data.
        """
        url = f"https://archive-api.open-meteo.com/v1/era5?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
        response = requests.get(url)
        data = json.loads(response.text)
        return data["hourly"]

set_model(NewAgent([{'function': {'name': 'get_current_weather', 'description': 'This function takes the latitude and longitude of a location as input and returns the current weather.\n    \n    ', 'parameters': {'properties': {'latitude': {'type': 'number', 'description': 'The latitude of the location.'}, 'longitude': {'type': 'number', 'description': 'The longitude of the location.'}}, 'type': 'object'}, 'strict': True}, 'type': 'function'}, {'function': {'name': 'get_hourly_forecast', 'description': 'This function takes the latitude and longitude of a location as input and returns the hourly forecast.\n    \n    ', 'parameters': {'properties': {'latitude': {'type': 'number', 'description': 'The latitude of the location.'}, 'longitude': {'type': 'number', 'description': 'The longitude of the location.'}}, 'type': 'object'}, 'strict': True}, 'type': 'function'}, {'function': {'name': 'get_historical_weather', 'description': 'This function takes the latitude, longitude, start date, and end date as input and returns the historical weather data.\n    \n    ', 'parameters': {'properties': {'latitude': {'type': 'number', 'description': 'The latitude of the location.'}, 'longitude': {'type': 'number', 'description': 'The longitude of the location.'}, 'start_date': {'type': 'string', 'description': 'The start date for which to retrieve the historical weather data.'}, 'end_date': {'type': 'string', 'description': 'The end date for which to retrieve the historical weather data.'}}, 'type': 'object'}, 'strict': True}, 'type': 'function'}], ['get_current_weather', 'get_hourly_forecast', 'get_historical_weather']))