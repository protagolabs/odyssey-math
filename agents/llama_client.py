import os
import time
import traceback
import json
from typing import Dict

from gradio_client import Client

class llama2_GradioAPIClient:
    """
    The Gradio API client which uses a custom API to generate responses to plain text messages.
    """

    client: Client
    api_url: str
    default_params: dict
    last_request_time: float

    def __init__(self, api_url: str, **default_params):
        """
        Initializes the GradioAPIClient.

        Parameters
        ----------
        api_url : str
            The URL of the Gradio API endpoint.
        """
        self.api_url = api_url
        self.client = Client(api_url)
        self.default_params = {
            "param_3": 0.9,
            "param_4": 1024,
            "param_5": 10
        }
        self.default_params.update(default_params)

    def run(self, message: str, request_description: str) -> Dict[str, str]:
        """
        Run the assistant with a given plain text message.

        Parameters
        ----------
        message : str
            The user message to be processed by the API.
        request_description : str
            The description of how the API should handle the message.

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
        params.update({
            "message": message,
            "request": request_description,
            "api_name": "/chat"  # Assuming '/chat' is the endpoint for message handling
        })

        count = 0
        while count < 10:
            try:
                result = self.client.predict(**params)
                try:
                    # Attempt to parse the result as JSON
                    result_dict = json.loads(result)
                    # Extract text content from JSON
                    text = result_dict.get('text', '')
                except json.JSONDecodeError:
                    # If result is not JSON, use it directly
                    text = result

                return {"content": text}
            except Exception as e:
                count += 1
                error_message = traceback.format_exc()
                print(f"Attempt {count}: An error occurred - {error_message}")
                time.sleep(2)  # Wait for 2 seconds before retrying

        raise Exception("Failed to get a response from the API after several attempts.")

# Example of using the GradioAPIClient
if __name__ == "__main__":
    api_url = "https://2c76d788cbff087d88-llama2-70b.test-playground-inference-2.netmind.ai/"
    client = llama2_GradioAPIClient(api_url)
    response = client.run(
        message="""
                The given text is:

                'Please Fill Out the Loan Application\nPersonal Information:\nFirst Name:\n\\(\\quad\\)Sophia\n\\(\\quad\\)Last Name:\n\\(\\quad\\)Martinez\n\\(\\quad\\)Social Security Number:\n\\(\\quad\\)N/A\n\\(\\quad\\)Date of Birth:\n\\(\\quad\\)N/A\n\\(\\quad\\)Email:\n\\(\\quad\\)sophia.martinez.fake@example.com\n\\(\\quad\\)Phone:\n\\(\\quad\\)\\( 555-1234 \\)\n\\(\\quad\\)Address:\n\\(\\quad\\)3300 Sunset Blvd, Apt 12, Los Angeles,\n\\(\\quad\\)CA 90026\n\\(\\quad\\)Marital Status:\n\\(\\quad\\)N/A\nEmployment and Financial Information:\n\\(\\quad\\)Employment Status:\n\\(\\quad\\)Employed\n\\(\\quad\\)Employer Name:\n\\(\\quad\\)N/A\n\\(\\quad\\)Annual Income:\n\\(\\quad\\)75000\n\\(\\quad\\)Other Income:\n\\(\\quad\\)0\n\\(\\quad\\)Monthly Expenses:\n\\(\\quad\\)5000\nLoan Requirement Details:\n\\(\\quad\\)Desired Loan Amount:\n\\(\\quad\\)30000\n\\(\\quad\\)Loan Purpose:\n\\(\\quad\\)Debt Consolidation\n\\(\\quad\\)Preferred Loan Term (in years):\n\\(\\quad\\)5\n\\(\\quad\\)Interest Rate (optional):\n\\(\\quad\\)\\( 6 \\% \\)\nSubmit Application'
                """,
        request_description="""Now, you are a Audit assistant who can help user to extract information from text.
    ## You must follow all the requirements to modify the draft:
        1. You must extract the name of person from the text, including first and last name.
        2. You must extract the period_covered from the text, if given.
        3. You must extract the address from the text, if given.
        4. You must extract the Opening Balance from the text, if given.
        5. You must extract the Closing Balance from the text only if given.
        6. You must extract the loan amount from the text only if the text is about loan application.
    
    ## About the output:
        Your output must be a json file containing a python dictionary to store the extracted information in the format looks like this: 
        
        {{
            "name": "xxx",
            "period_covered": "xxx",
            "address": "xxx",
            "period_covered": "xxx",
            "opening_balance": "xxx",
            "closing_balance": "xxx",
            "loan_amount": "xxx",
        }}
        You must follow all requirements listed above. 
        Your output must contain the json file quoted by "```json" and "```"

    """
    )
    print(response)
