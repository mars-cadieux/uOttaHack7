import asyncio
from crawl4ai import *
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.groq import GroqModel
import nest_asyncio
from openai import OpenAI
import one_shot_example

nest_asyncio.apply()

model = GroqModel('llama-3.1-70b-versatile', api_key='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')
agent = Agent(model, system_prompt='Be a helpful agent.')

USER_PROMPT = """
The provided 'retrieve_markdown' tool returns documation for the task you specify.
Make use of this tool to obtain an API or library for getting country-specific university data and write some functions using it.
AFTER CALLING 'retrieve_markdown':
It us up to you how many functions there should be, but they should serve a single and specific purpose. 
Make sure to follow these instructions:\n'
""" + one_shot_example.INSTRUCTIONS

async def main():
    result = agent.run_sync(USER_PROMPT)
    print(result.data)

@agent.tool
async def retrieve_markdown(ctx: RunContext[str]) -> str:
    print("called")
    """retrieve_markdown: Finds relevant APIs or libraries related to the input string and returns the content of those webpages in markdown format."""
    inputURL = 'https://github.com/Hipo/university-domains-list-api' #insert logic to find correct url
    async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(
                url=inputURL,
            )
            return result.markdown

if __name__ == "__main__":
    asyncio.run(main())