import serpapi

results = []

def main():
    getResults()

def getResults(query):
    params = {
    "engine": "google",
    "q": "Free news summary API or Python library for " + query,
    "api_key": "YOUR_KEY_HERE"
    }
    search = serpapi.search(params)
    for i in range(4):
        results.append(search["organic_results"][i]["link"])
    return results

def getSingleResult(query):
    params = {
    "engine": "google",
    "q": "Free news summary API or Python library for " + query,
    "api_key": "YOUR_KEY_HERE"
    }
    search = serpapi.search(params)
    result = search["organic_results"][0]["link"]
    return result
