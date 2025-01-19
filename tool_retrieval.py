import asyncio
from crawl4ai import *
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.groq import GroqModel
import nest_asyncio
from openai import OpenAI
import one_shot_example
from llm_crawler import CrawlExtract

nest_asyncio.apply()

MODEL = 'llama3-70b-8192'
client = OpenAI(api_key="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",
                        base_url="https://api.groq.com/openai/v1")

USER_PROMPT = """
You will use the provided JSON which describes an API or library to generate functions in Python that utilize it.
It us up to you how many functions there should be, but they should serve a single and specific purpose. 
There may be other URLs included in the JSON which you can further dig in for information using the provided tool.
Make sure to follow these instructions:
""" + \
one_shot_example.INSTRUCTIONS + \
""" Here is an example response after you get the markdown\n********\nSAMPLE RESPONSE:\n """ + \
one_shot_example.SAMPLE_RESPONSE + \
""" \n********\nCreate a response following the example and instructions above, but using the following JSON. You can also use the tool with one of the URLs in this text.\n"""


async def createPythonTools(inputURL: str):
    retrieved_markdown = await CrawlExtract(inputURL)
    tools = [{
        "type": "function",
        "function": {
            "name": "CrawlExtract",
            "description": "Extract information related to the API or library from the input URL",
            "parameters": {
                "type": "object",
                "properties": {
                    "URL": {
                        "type": "string",
                        "description": "URL to extract information from"
                    }
                },
                "URL": [
                    "URL"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    }]
    PROMPT = USER_PROMPT + retrieved_markdown
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{'role': 'system', 'content': 'Be a helpful agent.'}, {'role': 'user', 'content': PROMPT}],
        tools=tools
    )
    tool_calls = response.choices[0].message.tool_calls
    count = 0
    while(tool_calls and count < 5):
        for tool_call in tool_calls:
            PROMPT = PROMPT + await CrawlExtract(tool_call.function.arguments['URL'])
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{'role': 'system', 'content': 'Be a helpful agent.'}, {'role': 'user', 'content': PROMPT}],
            tools=tools
        )
        count = count + 1
        tool_calls = response.choices[0].message.tool_calls

    return response.choices[0].message.content
 

# if __name__ == "__main__":
#     asyncio.run(main())