import os
import asyncio
import json
from pydantic import BaseModel, Field
from typing import List
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import LLMExtractionStrategy

async def CrawlExtract(base_url: str):
    llm_strategy = LLMExtractionStrategy(
        provider="groq/llama3-8b-8192",           
        api_token="YOUR_KEY_HERE",          
        extraction_type="schema",
        instruction="Extract all information relevant to utilizing the API or library in Python",
        chunk_token_threshold=1000,
        overlap_rate=0.0,
        apply_chunking=True,
        input_format="markdown",   
        extra_args={"temperature": 0.0, "max_tokens": 1000}
    )

    crawl_config = CrawlerRunConfig(
        extraction_strategy=llm_strategy,
        cache_mode=CacheMode.BYPASS
    )

    browser_cfg = BrowserConfig(headless=True)

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        result = await crawler.arun(
            url=base_url,
            config=crawl_config,
            simulate_user=True,  
            override_navigator=True  
        )
        if result.success:
            return str(result.extracted_content)

        else:
            print("No data found")

# if __name__ == "__main__":
#     asyncio.run(CrawlExtract("https://www.newscatcherapi.com/blog/top-4-free-and-open-ource-news-api-alternatives"))