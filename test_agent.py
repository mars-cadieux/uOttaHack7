import mlflow
import os
from time import sleep
import requests
from generated_agent import NewAgent

with mlflow.start_run():
    model_info = mlflow.pyfunc.log_model(
        artifact_path="new_model",
        python_model=NewAgent(tools, functions),
        # input_example=input_example,
    )

    modeul_uri = model_info.model_uri
os.system(f"export OPENAI_API_KEY=ENTER_KEY_HERE")
os.system(f"mlflow models serve -m {modeul_uri}")
sleep(5)
messages = [
    {"role": "user", "content": "Tell me a joke"},
]

response = requests.post("http://127.0.0.1:5000/invocations", json={"messages": messages})
response.raise_for_status()
print(response.json())