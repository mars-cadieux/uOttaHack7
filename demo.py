#$START$
import requests
import json
#$END$

def get_gdelt_news_data(url):
    """
    This function takes a URL as input and returns the news data from GDELT 2.0 Global Knowledge Graph.
    
    Parameters:
    url (str): The URL of the GDELT 2.0 Global Knowledge Graph dataset.
    
    Returns:
    dict: A dictionary containing the news data.
    """
    response = requests.get(url)
    data = json.loads(response.text)
    return data

def get_common_crawl_news_data(url):
    """
    This function takes a URL as input and returns the news data from News Crawl by Common Crawl.
    
    Parameters:
    url (str): The URL of the News Crawl by Common Crawl dataset.
    
    Returns:
    dict: A dictionary containing the news data.
    """
    response = requests.get(url)
    data = json.loads(response.text)
    return data

def get_rss_feed_news_data(url):
    """
    This function takes a URL as input and returns the news data from an RSS feed.
    
    Parameters:
    url (str): The URL of the RSS feed.
    
    Returns:
    dict: A dictionary containing the news data.
    """
    response = requests.get(url)
    data = json.loads(response.text)
    return data

def get_google_news_rss_data(url):
    """
    This function takes a URL as input and returns the news data from Google News (RSS).
    
    Parameters:
    url (str): The URL of the Google News RSS feed.
    
    Returns:
    dict: A dictionary containing the news data.
    """
    response = requests.get(url)
    data = json.loads(response.text)
    return data
