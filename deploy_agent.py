import mlflow
import os
from time import sleep
import requests
from generated_agent import NewAgent

with mlflow.start_run():
    model_info = mlflow.pyfunc.log_model(
        artifact_path="new_model",
        python_model=NewAgent(),
    )

    model_uri = model_info.model_uri
os.system(f"mlflow models serve -m {model_uri} --port 5001")