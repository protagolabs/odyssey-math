import os
import time
import traceback
import json
from typing import Dict
import re
import time

from agents.llama_client import Llama3APIClient
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()
api_token = os.getenv('Netmind_API_KEY')


api_url = "https://inference-api.netmind.ai/inference-api/v1/llama3-70B"

client = Llama3APIClient(api_url, api_token)
request = """
    You are now assuming the role of a math professor. Your task is to assist the user by solving complex mathematical problems in a detailed and step-by-step manner.

    ## Task Requirements:
    1. **Detailed Problem Analysis**: Start by analyzing the given problem. Identify and articulate the key mathematical concepts and techniques needed to solve the problem.
    2. **Step-by-Step Solution**: Decompose the problem into manageable steps. Solve each step sequentially, ensuring logical progression and coherence in your approach.
    3. **Theoretical Justification**: For each step, provide a clear explanation of the mathematical theories or principles applied. Justify your choice of method and demonstrate how it applies to the specific problem at hand.
    4. **Calculation Verification**: After solving each step, verify your calculations. Explain any checks or balances you use to ensure the accuracy of your computations.
    5. **Error Checking and Assumptions**: State any assumptions made during the solution process. Discuss potential errors or alternative methods that could impact the solution.
    6. **Conclusive Summary**: Conclude with a summary of how the steps tie together and confirm the solution's validity.

    ## Expected Output Format:
    Present your final answer and the complete solution process in a JSON format. This should include:
        - A `float` value or a mathematical algebraic expression for the answer.
        - Detailed reasoning for each step of the solution.

    Your output should be formatted as a JSON object enclosed in Markdown code blocks tagged with 'json'. For example:
    
    ```json
    {{
        "answer": "<answer>",
        "reasoning": "<detailed solution process>"
    }}
    ```
    Ensure that all task requirements are meticulously followed in your response.
"""

def process_math_problems(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            time.sleep(2)
            status = 0
            problem = json.loads(line)  # Convert JSON line to dictionary
            for key, value in problem.items():
                question = value['question']
                question =  "The given question is:   \n" + question
                messages = [
                    {
                        "role": "system",
                        "content": request
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ]
                while status == 0:
                    try:
                        response = client.run(
                            messages
                        )
                        response = response['content']
                        status = 1
                    except:
                        time.sleep(10)
                        status = 0
                
                output_json = json.dumps({key: response})  # Convert response to JSON line
                outfile.write(output_json + '\n')  # Write to file

# Specify your input and output files
input_file_path = 'final-odyssey-math-with-levels.jsonl'
output_file_path = 'jsonl/llama3-70b-solution.jsonl'

# Call the processing function
process_math_problems(input_file_path, output_file_path)