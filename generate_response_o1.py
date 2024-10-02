import json
from openai import OpenAI
from dotenv import load_dotenv
import os
import copy

# Load the environment variables from the .env file
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client_openai = OpenAI(api_key=OPENAI_API_KEY)

def run_openai(messages, client):
    
    # Send the prompt to OpenAI's GPT-4
    response = client.chat.completions.create(
        model="o1-preview",
        messages=messages,
    )

    answer = response.choices[0].message.content
    
    return answer

def generate_feature_engineer_templates(SOLUTION, question):
    """
    Generates FEATURE_ENGINEER template with substituted texts.
    
    """

    # Deep copy the original template to avoid modifying it
    updated_template = copy.deepcopy(SOLUTION)
        
    # Substitute the placeholder in the user document
    for entry in updated_template:
        if entry["role"] == "user":
            entry["content"] = entry["content"].format(question=question)
    
    return updated_template

SOLUTION = [
    {
        "role": "user",
        "content": """
            Please help me solve the given math question.

            ## Expected Output Format:
            Present your final answer in a JSON format. This should include:
                - A `float` value or a mathematical algebraic expression for the answer.

            Your output should be formatted as a JSON object enclosed in Markdown code blocks tagged with 'json'. For example:
            
            ```json
            {{
                "answer": "<answer>",
            }}
            ```
            "Here is the question: {question}."
        """
    }
]


def process_math_problems(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            problem = json.loads(line)  # Convert JSON line to dictionary
            for key, value in problem.items():
                question = value['question']
                updated_template = generate_feature_engineer_templates(SOLUTION, question)
                response = run_openai(updated_template, client_openai)
                output_json = json.dumps({key: response})  # Convert response to JSON line
                outfile.write(output_json + '\n')  # Write to file

# Specify your input and output files
input_file_path = 'final-odyssey-math-with-levels.jsonl'
output_file_path = 'jsonl/gpt-4-o1-preview-solution.jsonl'

# Call the processing function
process_math_problems(input_file_path, output_file_path)