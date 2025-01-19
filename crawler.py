import asyncio
from crawl4ai import *
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.groq import GroqModel
import nest_asyncio
nest_asyncio.apply()

model = GroqModel('llama-3.1-70b-versatile', api_key='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')
agent = Agent(model, system_prompt='Be a helpful agent.',)

async def main():
    result = agent.run_sync('Show me markdown for a webpage that gives instructions on how to use its API to get live weather data. Write me a Python function that calls this API.')
    print("Result 1: " + result.data)

@agent.tool
async def scrape(ctx: RunContext[str]) -> str:
    """Finds relevant APIs or libraries related to the input string and returns the content of those webpages in markdown format."""
    inputURL = 'https://open-meteo.com/' #insert logic to find correct url
    async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(
                url=inputURL,
            )
            return result.markdown

if __name__ == "__main__":
    asyncio.run(main())