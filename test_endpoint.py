import requests

messages = [
    {"role": "system", "content": "Please use the provided tools to answer user queries. If the tool output has lots of data do not try to summarize the results in any way, in this case just tell the user to refer to the tool outputed (provided in a previous response)."},
    {"role": "user", "content": "Tell me about pokemon id=132?"},
]

response = requests.post("http://127.0.0.1:5001/invocations", json={"messages": messages})
response.raise_for_status()
print(response.json())