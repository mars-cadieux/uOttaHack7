#$START$
import requests
#$END$

### Search for universities by name and country
"""
This function searches for universities by name and country.
It takes in two parameters: name and country.
The name parameter is required, while the country parameter is optional.
The function returns a list of universities that match the search criteria.
"""
def search_universities(name, country=None):
    url = "http://universities.hipolabs.com/search"
    params = {"name": name}
    if country:
        params["country"] = country
    response = requests.get(url, params=params)
    return response.json()

### Update the university dataset
"""
This function updates the university dataset using the API's update endpoint.
It takes in no parameters.
The function returns a dictionary containing the status and message of the update operation.
"""
def update_university_dataset():
    url = "http://universities.hipolabs.com/update"
    response = requests.get(url)
    return response.json()

### Get a university by its name
"""
This function gets a university by its name.
It takes in one parameter: name.
The function returns a dictionary containing the university's information.
"""
def get_university_by_name(name):
    universities = search_universities(name)
    if universities:
        return universities[0]
    else:
        return None

### Get universities by their country
"""
This function gets universities by their country.
It takes in one parameter: country.
The function returns a list of universities that are located in the specified country.
"""
def get_universities_by_country(country):
    url = "http://universities.hipolabs.com/search"
    params = {"country": country}
    response = requests.get(url, params=params)
    return response.json()

print(search_universities("Carleton University"))