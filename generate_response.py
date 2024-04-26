from agents.solve import mathSolve
import json

def process_math_problems(input_file, output_file):
    msv = mathSolve()  # Initialize your solving class
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            problem = json.loads(line)  # Convert JSON line to dictionary
            for key, value in problem.items():
                question = value['question']
                response = msv(question=question)  # Solve the problem
                output_json = json.dumps({key: response})  # Convert response to JSON line
                outfile.write(output_json + '\n')  # Write to file

# Specify your input and output files
input_file_path = 'final-odyssey-math-with-levels.jsonl'
output_file_path = 'jsonl/gpt-4-0125-preview-solution.jsonl'

# Call the processing function
process_math_problems(input_file_path, output_file_path)