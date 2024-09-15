"""
=======
solve
=======
@date: 2024-4-24
"""
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import numpy as np
from xyz.node.agent import Agent
from xyz.node.basic.llm_agent import LLMAgent
from xyz.utils.llm.openai_client import OpenAIClient
import os
import json
import re
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class mathSolve(Agent):
    def __init__(self):
        
        super().__init__()  

        self.openai_agent = OpenAIClient(api_key=OPENAI_API_KEY, model='gpt-4-0613', temperature=0., top_p=0.8)
        self.llm_evaluate_agent = LLMAgent(SOLUTION, self.openai_agent, stream=False)

    def extract_dict_from_json(self,text: str):
        """
        Extract the dictionary between "```json" and "```". 
        """
        pattern = r'```json(.*?)```'
        extracted_text = re.findall(pattern, text, re.DOTALL)

        return extracted_text[0].strip() 

    def flowing(self, question: str) -> str:

        
        result = self.llm_evaluate_agent(question=question)
        try:
            result = self.extract_dict_from_json(result)
        except:
            pass

        return result


SOLUTION = [
    {
        "role": "system",
        "content": """
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
                "reasoning": "<detailed solution process>",
                "answer": "<answer>",
            }}
            ```
            Ensure that all task requirements are meticulously followed in your response.
        """
    },
    {
        "role": "user",
        "content": "Here is the question: {question}."
    }
]

# Example of using the mathSolve
if __name__ == "__main__":
    
    msv = mathSolve()
    response = msv(question="What is the sum of 2 and 2?")