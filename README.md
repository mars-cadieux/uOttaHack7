# Overview

The API Agent project is a Python-based solution that enhances the capabilities of an AI system by integrating external data sources through API communication and web scraping. The project includes a user-friendly UI design, making it accessible to a broader audience.

This system enables the AI to answer user queries by fetching real-time data from external APIs or websites. For example, when asked, "What's the weather today in Paris?", the AI leverages API Agents to gather the required data and provides an accurate response. If the AI does not have an agent on hand that can answer the user's question, the AI will employ a web crawler to search for an API to leverage, then will instatiate an AI Agent which generates a function to make the API call, then will add this function to its set of available tools. On the surface, this gives the user the impression of interacting with a self-training AI model. 




## Built With



[![MIT License](https://img.shields.io/badge/python-3.x-blue?logo=python&logoColor=white)](https://www.python.org/)


## Installation

- Python 3.8+
- pip (Python package manager)
- A code editor or IDE (e.g., VS Code, PyCharm) for running and debugging the project.
- Clone this repository
- Install necessary dependencies
- Add your API keys
- In your terminal, run 'python demo.py'

## Explore the UI

Navigate to https://agent-app-ui--development.gadget.app/ and interact with our agent in a seamless manner on our beautiful layout.

    
## API Key

You will need to generate a free API key from both https://serpapi.com/ and https://openai.com/

## 🔗 Links

[![Github](https://img.shields.io/badge/GitHub-000?logo=github&logoColor=white)](https://github.com/mars-cadieux/uOttaHack7/tree/main)
