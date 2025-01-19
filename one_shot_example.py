MARKDOWN = """
[Open-Meteo](https://open-meteo.com/</>)
  * [Home](https://open-meteo.com/</> "Weather API")
  * [Features](https://open-meteo.com/</en/features> "API Features")
  * [Pricing](https://open-meteo.com/</en/pricing> "Pricing")
  * [API Docs](https://open-meteo.com/</en/docs> "Documentation")


  * [ GitHub](https://open-meteo.com/<https:/github.com/open-meteo/open-meteo>)
  * [ Twitter](https://open-meteo.com/<https:/twitter.com/open_meteo>)
  * Toggle theme
    * Light
    * Dark
    * Auto


# Free Weather API
Open-Meteo is an open-source weather API and offers free access for non-commercial use. No API key required. Start using it now!
[Features](https://open-meteo.com/</en/features>) [Try the API here!](https://open-meteo.com/</en/docs>)
## Accurate Weather Forecasts for Any Location
Open-Meteo partners with national weather services to bring you open data with high resolution, ranging from 1 to 11 kilometers. Our powerful APIs intelligently select the most suitable weather models for your specific location, ensuring accurate and reliable forecasts.
With our user-friendly JSON API, accessing weather data has never been easier. Whether you're developing an application or seeking weather information for personal use, our APIs provide seamless integration and deliver the data you need in a simple and accessible format.
Experience the precision and convenience of Open-Meteo's Forecast API, providing comprehensive weather information worldwide. Stay informed and make informed decisions with our reliable weather forecasts.
[See features](https://open-meteo.com/</en/features>) [Read the docs](https://open-meteo.com/</en/docs>)
  * Forecast & Current
  * Last 10 days
  * Historical data


$ curl ["https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"](https://open-meteo.com/<https:/api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m>)
```
{
 "current": {
  "time": "2022-01-01T15:00"
  "temperature_2m": 2.4,
  "wind_speed_10m": 11.9,
 },
 "hourly": {
  "time": ["2022-07-01T00:00","2022-07-01T01:00", ...]
  "wind_speed_10m": [3.16,3.02,3.3,3.14,3.2,2.95, ...],
  "temperature_2m": [13.7,13.3,12.8,12.3,11.8, ...],
  "relative_humidity_2m": [82,83,86,85,88,88,84,76, ...],
 }
}
```

### High Resolution
Open-Meteo leverages a powerful combination of global (11 km) and mesoscale (1 km) weather models from esteemed national weather services, providing comprehensive forecasts with remarkable precision. No matter where you are in the world, you can access the most reliable and accurate weather predictions available.
Our weather data is presented in hourly resolution, allowing you to plan your activities with confidence. The initial days of the forecast benefit from localized weather models, offering highly detailed and accurate information. Subsequently, global weather models provide forecasts for up to 16 days. Through seamless integration, our APIs deliver a straightforward and reliable hourly weather forecast experience.
### Rapid Updates
At Open-Meteo, we understand the importance of having the most up-to-date weather information. That's why our local weather models are updated every hour, ensuring that our forecasts reflect the latest changes in conditions, including updates from rain radars.
Our weather models rely on a wealth of real-time data, including measurements from various sources such as airplanes, buoys, radar systems, and satellites. By incorporating this diverse and comprehensive data, our numerical weather predictions provide a deeper analysis than traditional weather stations, resulting in more accurate forecasts.
### 80 Years Historical Data
Explore the past with our comprehensive [Historical Weather API](https://open-meteo.com/</en/docs/historical-weather-api> "Historical weather data via API"). With over 80 years of hourly weather data available at a 10 kilometer resolution, you can dive into the climate of any location. Behind the scenes, this extensive dataset, comprising 50 TB of information, enables you to access temperature records spanning eight decades in an instant.
Moreover, our 1 kilometer weather models continuously archive recent data, ensuring that you can seamlessly retrieve the latest forecasts alongside historical information from previous weeks. This functionality opens up possibilities for training machine learning applications and gaining valuable insights from the combination of present and past weather data. Discover the power of our historical weather API and unlock a treasure trove of weather information.
### Open-Source
We believe in the power of open-source software. That's why the entire codebase of Open-Meteo is accessible on [GitHub](https://open-meteo.com/<https:/github.com/open-meteo/open-meteo> "Open-Meteo GitHub respository"), released under the [AGPLv3 licence](https://open-meteo.com/<https:/github.com/open-meteo/open-meteo/blob/main/LICENSE>). This means you can explore, use, modify, and contribute to the code.
If you wish to take it a step further, we're here to support you in setting up your own API instances. This allows you to have complete control and enjoy practically unlimited API calls, making it ideal for demanding applications like machine learning or large language models.
In addition, our data is licensed under [Attribution 4.0 International (CC BY 4.0)](https://open-meteo.com/<https:/creativecommons.org/licenses/by/4.0/> "CC BY 4.0 Licence Information"). This means you are free to share and adapt the data, even for commercial purposes. We believe in fostering an open ecosystem that encourages transparency, collaboration and innovation.
### Free API
Open-Meteo offers free access to its APIs for non-commercial use, making it convenient for individuals and developers to explore and integrate weather data into their projects. The best part is that no API key, registration, or credit card is required to enjoy this service.
We trust our users to utilize the free API responsibly and kindly request appropriate credit for the data used. While there are no strict access restrictions, we encourage fair usage of the service. If you require commercial usage or anticipate exceeding 10'000 API calls per day, we recommend considering our [API subscription](https://open-meteo.com/</en/pricing> "Pricing for our paid API subscription") for enhanced features and support.
### Easy to Use
We've designed our APIs to be incredibly user-friendly. They are based on the widely adopted HTTP protocol and utilize the simplicity of JSON data format. All you need to get started is a basic understanding of geographic coordinates, making HTTP requests, and working with JSON data.
To assist you in seamlessly integrating our APIs into your projects, we provide comprehensive [documentation](https://open-meteo.com/</en/docs> "Weather API Technical Documentation"). It includes detailed explanations of all parameters and their usage. Whether you're using Python, R, Julia, PHP, JavaScript, React, Flutter, Java, or any other programming language, our APIs are designed to work effortlessly with your application.
# Stay up to date!
We're constantly evolving and expanding. We're dedicated to providing you with the [latest features](https://open-meteo.com/</en/features> "All Features of the Weather API"), weather variables, and data sources. If you want to stay in the loop and be the first to know about our exciting updates, we invite you to subscribe to our [blog](https://open-meteo.com/<https:/openmeteo.substack.com/archive?sort=new>) or follow us on [Twitter](https://open-meteo.com/<https:/twitter.com/open_meteo>). By doing so, you'll never miss out on the latest developments and enhancements in our services.
[Subscribe to the Newsletter](https://open-meteo.com/<https:/openmeteo.substack.com/subscribe?utm_source=landingpage&simple=true&next=https%3A%2F%2Fopenmeteo.substack.com%2F> "Newsletter Sign-Up") [Available APIs](https://open-meteo.com/</en/features> "APIs & Features")
Open-Meteo
  * [Features](https://open-meteo.com/</en/features>)
  * [Pricing](https://open-meteo.com/</en/pricing>)
  * [About us & Contact](https://open-meteo.com/</en/about>)
  * [License](https://open-meteo.com/</en/license>)
  * [Terms & Privacy](https://open-meteo.com/</en/terms>)


Weather APIs
  * [Weather Forecast API](https://open-meteo.com/</en/docs>)
  * [Historical Weather API](https://open-meteo.com/</en/docs/historical-weather-api>)
  * [ECMWF API](https://open-meteo.com/</en/docs/ecmwf-api>)
  * [GFS & HRRR Forecast API](https://open-meteo.com/</en/docs/gfs-api>)
  * [Météo-France API](https://open-meteo.com/</en/docs/meteofrance-api>)
  * [DWD ICON API](https://open-meteo.com/</en/docs/dwd-api>)
  * [GEM API](https://open-meteo.com/</en/docs/gem-api>)
  * [JMA API](https://open-meteo.com/</en/docs/jma-api>)
  * [Met Norway API](https://open-meteo.com/</en/docs/metno-api>)


Other APIs
  * [Ensemble API](https://open-meteo.com/</en/docs/ensemble-api>)
  * [Climate Change API](https://open-meteo.com/</en/docs/climate-api>)
  * [Marine Weather API](https://open-meteo.com/</en/docs/marine-weather-api>)
  * [Air Quality API](https://open-meteo.com/</en/docs/air-quality-api>)
  * [Geocoding API](https://open-meteo.com/</en/docs/geocoding-api>)
  * [Elevation API](https://open-meteo.com/</en/docs/elevation-api>)
  * [Flood API](https://open-meteo.com/</en/docs/flood-api>)


External
  * [GitHub](https://open-meteo.com/<https:/github.com/open-meteo/open-meteo>)
  * [Blog](https://open-meteo.com/<https:/openmeteo.substack.com/archive?sort=new>)
  * [Twitter](https://open-meteo.com/<https:/twitter.com/open_meteo>)
  * [Mastodon](https://open-meteo.com/<https:/fosstodon.org/@openmeteo>)
  * [Service status and uptime](https://open-meteo.com/<https:/status.open-meteo.com>)
  * [Model Updates Overview](https://open-meteo.com/</en/docs/model-updates>)


© 2022-2025 Copyright: Open-Meteo.com
"""

SAMPLE_RESPONSE = """
REASONING:
The 'retrieve_markdown' tool returned information on the Open-Meteo API, a free weather API that provides current and forecasted weather data. I chose to create functions that serve specific purposes, such as getting the current weather, getting the hourly forecast, and getting the historical weather data. These functions meet the requirement of being modular because they can be used independently of each other and can be easily combined to achieve more complex tasks.

CODE:
#$START$
import requests
import json
#$END$

### \"""Gets the current weather for a given location.\"""
def get_current_weather(latitude, longitude):
    \"""
    This function takes the latitude and longitude of a location as input and returns the current weather.
    
    Parameters:
    latitude (float): The latitude of the location.
    longitude (float): The longitude of the location.
    
    Returns:
    dict: A dictionary containing the current weather data.
    \"""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    response = requests.get(url)
    data = json.loads(response.text)
    return data["current_weather"]

### \"""Gets the hourly forecast for a given location.\"""
def get_hourly_forecast(latitude, longitude):
    \"""
    This function takes the latitude and longitude of a location as input and returns the hourly forecast.
    
    Parameters:
    latitude (float): The latitude of the location.
    longitude (float): The longitude of the location.
    
    Returns:
    dict: A dictionary containing the hourly forecast data.
    \"""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
    response = requests.get(url)
    data = json.loads(response.text)
    return data["hourly"]

### \"""Gets the historical weather data for a given location and date.\"""
def get_historical_weather(latitude, longitude, date):
    \"""
    This function takes the latitude, longitude, and date as input and returns the historical weather data.
    
    Parameters:
    latitude (float): The latitude of the location.
    longitude (float): The longitude of the location.
    date (str): The date for which to retrieve the historical weather data.
    
    Returns:
    dict: A dictionary containing the historical weather data.
    \"""
    url = f"https://archive-api.open-meteo.com/v1/era5?latitude={latitude}&longitude={longitude}&start_date={date}&end_date={date}&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
    response = requests.get(url)
    data = json.loads(response.text)
    return data["hourly"]
"""

INSTRUCTIONS = """
-Your functions must be based around the API/Library returned by the provided tool
-After 'REASONING:' provide your reasoning for why you chose to break down your response
into the functions you did and how they meet the requirement of being modular  
-Everything after 'CODE:' should be an executable Python file, and nothing else
-All import statements must be included at the top of your response
-'#$START$' should come before all import statements
-'#$END$' should come immediately after the final import statement
-The rest of the file should be the sequence of python functions using the API/library
-Above each function include a brief description of the function inside inside triple quotes
-The description should go into detail about each of the inputs and the purpose of the function
"""