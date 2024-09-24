import os
import uuid
import requests
from promptflow.core import tool


@tool
def translate_text(text: str, from_lang: str, to_lang: str) -> str:
    path = "/translate"
    endpoint = os.getenv("AI_TRANSLATOR_ENDPOINT")
    constructed_url = endpoint + path

    params = {
        "api-version": "3.0",
        "from": from_lang,
        "to": [to_lang],  # Single language in a list
    }
    headers = {
        "Ocp-Apim-Subscription-Key": os.getenv("AI_TRANSLATOR_KEY"),
        "Ocp-Apim-Subscription-Region": "eastus2",
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }

    body = [{"text": text}]
    try:
        response = requests.post(
            constructed_url, params=params, headers=headers, json=body
        )
        response.raise_for_status()
        response_json = response.json()

        translated_text = response_json[0]["translations"][0]["text"]
        translated_to = response_json[0]["translations"][0]["to"]

        if translated_to == to_lang:
            return translated_text
        else:
            print(f"Unexpected translation language : {translated_to}")
            return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occured: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Error occurred: {req_err}")
    except Exception as err:
        print(f"An unexpected error occured: {err}")
