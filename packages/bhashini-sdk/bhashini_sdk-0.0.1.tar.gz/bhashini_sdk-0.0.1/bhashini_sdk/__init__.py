import os
from typing import List, TypedDict
import urllib.parse
import requests
import json

pipeline_task_0 = None
config = None


def pipeline_config(src_language: str, dest_language: str):
    global pipeline_task_0, config
    if pipeline_task_0 is None or config is None:
        tasks = [{"taskType": "translation"}]

        config_url = urllib.parse.urljoin(
            os.getenv("BHASHINI_MEITY_CONFIG_URL"),
            "ulca/apis/v0/model/getModelsPipeline",
        )

        payload = {
            "pipelineTasks": tasks,
            "pipelineRequestConfig": {"pipelineId": os.getenv("BHASHINI_PIPELINE_ID")},
        }

        headers = {
            "Content-Type": "application/json",
            "userID": os.getenv("BHASHINI_USER_ID"),
            "ulcaApiKey": os.getenv("BHASHINI_API_KEY"),
            "compute_call_authorization_key": "Authorization",
        }

        response = requests.post(config_url, data=json.dumps(payload), headers=headers)
        if response.status_code != 200:
            raise Exception("Error in getting config:" + response.text)

        config = response.json()

        pipeline_task_0 = next(
            (
                e
                for e in config["pipelineResponseConfig"][0]["config"]
                if e["language"]["sourceLanguage"] == src_language
                and e["language"]["targetLanguage"] == dest_language
            ),
            None,
        )

        return config, pipeline_task_0

    return config, pipeline_task_0


class TextToTextOutput(TypedDict):
    source: str
    target: str


class TextToTextResponse(TypedDict):
    taskType: str
    config: None
    output: List[TextToTextOutput]
    audio: str


def text_to_text(
    text: List[str], src_language: str, dest_language: str, retires=0, max_retries=10
) -> TextToTextResponse:
    print("Retry: ", retires)
    config, pipeline_task_0 = pipeline_config(src_language, dest_language)
    callback_url = config["pipelineInferenceAPIEndPoint"]["callbackUrl"]
    payload = {
        "pipelineTasks": [
            {
                "taskType": "translation",
                "config": {
                    "language": {
                        "sourceLanguage": src_language,
                        "targetLanguage": dest_language,
                    },
                    "serviceId": pipeline_task_0["serviceId"],
                },
            },
        ],
        "inputData": {
            "input": list(map(lambda x: {"source": x}, text)),
        },
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": config["pipelineInferenceAPIEndPoint"]["inferenceApiKey"][
            "value"
        ],
    }

    # Make the POST request
    try:
        response = requests.post(
            callback_url,
            data=json.dumps(payload),
            headers=headers,
            timeout=20,
        )
        if response.status_code != 200:
            print(response.status_code)
            print(response.text)
            if retires < max_retries:
                return text_to_text(text, src_language, dest_language, retires + 1)
            raise Exception("Error in translation")
    except Exception as e:
        # if read timeout, retry
        print(e)
        if retires < 10:
            return text_to_text(text, src_language, dest_language, retires + 1)
        raise Exception("Error in translation")

    response = response.json()
    return response["pipelineResponse"][0]
