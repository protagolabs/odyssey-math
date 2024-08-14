import os
import time
import traceback
import json
from typing import Dict

import requests

class Llama3APIClient:
    """
    The API client that uses a custom API to generate responses to plain text messages.
    """

    def __init__(self, api_url: str, api_token: str, **default_params):
        """
        Initializes the API client.

        Parameters
        ----------
        api_url : str
            The URL of the API endpoint.
        api_token : str
            The API token for authentication.
        """
        self.api_url = api_url
        self.api_token = api_token
        self.default_params = {
            "max_new_tokens": 2048,
            "temperature": 0.1,
            "top_p": 0.9,
            "top_k": 50,
            "repetition_penalty": 1.2,
        }
        self.default_params.update(default_params)

    def run(self, messages: list, **override_params) -> Dict[str, str]:
        """
        Run the assistant with a given plain text message.

        Parameters
        ----------
        messages : list
            A list of messages to be processed by the API.
        override_params : dict
            Parameters that will override the default parameters.

        Returns
        -------
        Dict[str, str]
            The API's response.

        Raises
        ------
        Exception
            If there is an error while making the request to the API.
        """
        params = self.default_params.copy()
        params.update(override_params)
        data = {
            "messages": messages,
            **params
        }

        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

        count = 0
        while count < 10:
            try:
                response = requests.post(self.api_url, headers=headers, data=json.dumps(data))
                response.raise_for_status()

                try:
                    # Attempt to parse the response as JSON
                    result_dict = response.json()
                    # Extract text content from JSON
                    text = result_dict.get('text', '')
                except json.JSONDecodeError:
                    # If result is not JSON, use it directly
                    text = response.text

                return {"content": text}
            except Exception as e:
                count += 1
                error_message = traceback.format_exc()
                print(f"Attempt {count}: An error occurred - {error_message}")
                time.sleep(2)  # Wait for 2 seconds before retrying

        raise Exception("Failed to get a response from the API after several attempts.")


if __name__ == "__main__":
    
    from dotenv import load_dotenv

    # Load the environment variables from the .env file
    load_dotenv()
    api_token = os.getenv('Netmind_API_KEY')


    api_url = "https://inference-api.netmind.ai/inference-api/v1/llama3-70B"

    client = Llama3APIClient(api_url, api_token)

    messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant."
    },
    {
        "role": "user",
        "content": "Write a 100-word article on 'Benefits of Open-Source in AI research'"
    }
]

    response = client.run(messages)
    print(response['content'])