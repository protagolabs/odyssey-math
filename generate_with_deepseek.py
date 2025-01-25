import os
import time
import traceback
import json
from typing import Dict
import re
import time

from openai import OpenAI
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()
api_token = os.getenv('NETMIND_POWER_KEY')

# Set up the client with the new OpenAI structure
client = OpenAI(
    base_url="https://api.netmind.ai/inference-api/openai/v1",
    api_key=api_token,
)

model = "deepseek-v3"
stream = False  # Set to True if you want streamed output
max_tokens = 2000

# Define the request prompt for solving math problems
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
        - Concise reasoning for obtaining the solution.
        - A `float` value or a mathematical algebraic expression for the answer.
        

    Your output should be formatted as a JSON object enclosed in Markdown code blocks tagged with 'json'. For example:
    
    ```json
    {{
        "reasoning": "<concise solution process>",
        "answer": "<answer>",
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
                question_prompt =  "The given question is:  \n" + question
                full_prompt = [
                    {"role": "system", "content": request},
                    {"role": "user", "content": question_prompt},
                ]
                
                while status == 0:
                    try:
                        chat_completion_response = client.chat.completions.create(
                            model=model,
                            messages=full_prompt,
                            stream=stream,
                            max_tokens=max_tokens,
                        )

                        response = chat_completion_response.choices[0].message.content
                        
                        status = 1  # Set status to 1 after successful completion
                    except Exception as e:
                        print(f"Error occurred for {key}: {e}")  # Print the error message
                        print("Retrying...")
                        time.sleep(10)
                        status = 0
                
                output_json = json.dumps({key: response})  # Convert response to JSON line
                outfile.write(output_json + '\n')  # Write to file

# Specify your input and output files
input_file_path = 'final-odyssey-math-with-levels.jsonl'
output_file_path = 'jsonl/deepseek-v3-Instruct-solution.jsonl'

# Call the processing function
process_math_problems(input_file_path, output_file_path)
