import asyncio
from crawl4ai import *
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.groq import GroqModel
import nest_asyncio
from openai import OpenAI
import one_shot_example

nest_asyncio.apply()

model = GroqModel('llama-3.1-70b-versatile', api_key='YOUR KEY HERE')
agent = Agent(model, system_prompt='Be a helpful agent.',)

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