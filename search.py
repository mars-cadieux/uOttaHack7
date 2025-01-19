import serpapi

params = {
  "engine": "google",
  "q": "Free weather API",
  "api_key": "YOUR KEY HERE"
}

results = []

def main():
    search = serpapi.search(params)
    for i in range(4):
        results.append(search["organic_results"][i]["link"])
    print(results)

if __name__ == "__main__":
    main()