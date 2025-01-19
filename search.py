import serpapi

params = {
  "engine": "google",
  "q": "Free news summary API or Python library",
  "api_key": "YOUR_KEY_HERE"
}

results = []

def main():
    search = serpapi.search(params)
    for i in range(4):
        results.append(search["organic_results"][i]["link"])
    print(results)

if __name__ == "__main__":
    main()