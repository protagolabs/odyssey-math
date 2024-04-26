"""
=======
result evaluator
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


class Evalutor(Agent):
    def __init__(self):
        
        super().__init__()  

        self.openai_agent = OpenAIClient(api_key=OPENAI_API_KEY, model='gpt-4-turbo-2024-04-09', temperature=0., top_p=0.8,
                                         max_tokens=2096)
        self.llm_evaluate_agent = LLMAgent(EVALUATION, self.openai_agent, stream=False)


    def flowing(self, question: str, true: str, prediction: str) -> str:
        
        result = self.llm_evaluate_agent(question=question, true=true, prediction=prediction)

        return result


EVALUATION = [
    {
        "role": "system",
        "content":
        """
        Assume the role of a math teacher tasked with evaluating student responses against the provided solutions, which may include exact values, multiple-choice answers, or numerical approximations. The question is provided as: {question}, the correct answer is provided as: {true}.
        
        ## Evaluation Criteria:
        1. **Mathematical Equivalence**: Evaluate answers based on deep mathematical equivalence, not just numerical accuracy. Use advanced tools or techniques to verify if different algebraic or symbolic expressions are equivalent. Tools like symbolic computation software (e.g., Wolfram Alpha, SymPy) should be used to confirm equivalences such as \\( \\frac{{\\sqrt{{6}}-\\sqrt{{2}}}}{{2}} \\) being equivalent to \\( \\sqrt{{2 - \\sqrt{{3}}}} \\).
        2. **Scoring**: Assign a score of '1' for any answer that matches or is equivalent to the provided solution, whether it is an exact value, a choice label (e.g., A, B, C), or a correctly rounded numerical approximation. Assign a score of '0' for incorrect answers. Do not provide any explanatory feedback in your evaluation.
        3. **Handling Multiple Choices**: If the solution provided is a choice (e.g., A, B, C, D, E, F) and the student identifies this choice correctly, treat it as correct. If the solution is an exact value and the student provides the corresponding choice that reflects this value correctly according to the problem's context, also treat it as correct.
        4. **Numerical Equivalence**: Treat numerical answers as equivalent if they are correct to at least two decimal places or more, depending on the precision provided in the solution. For instance, both 0.913 and 0.91 should be accepted if the solution is accurate within two decimal places.
        5. **Symbolic and Algebraic Identities**: Recognize and accept equivalent algebraic forms, such as \\( \\sin^2(x) + \\cos^2(x) = 1 \\) or \\( e^{{i\\pi}} + 1 = 0 \\), as correct.
        6. **Trigonometric and Logarithmic Forms**: Accept equivalent trigonometric and logarithmic expressions, acknowledging identities and transformations that might alter the form but not the value.
        7. **Comprehensive Evaluation**: Encourage the use of computational tools to check for equivalence in cases where expressions are too complex for straightforward visual inspection.

        ## Expected Output Format:
            Present your final answer with a score of '1' or '0' only. Do not include any additional information or feedback in your response.
        
        Please evaluate the student's response with precision, utilizing computational resources as necessary to ensure accurate and fair grading.
        """
    },
    {"role": "user", "content": 
    """
    The student answer is {prediction}.
    """
    }
]

# Example of using the mathSolve
if __name__ == "__main__":
    
    evaluation = Evalutor()
    response = evaluation(question="What is the sum of 2 and 2?",true="4",prediction="4")
