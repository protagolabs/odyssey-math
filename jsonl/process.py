import re
import json

# List of tuples containing input file paths and corresponding output file paths
# file_paths = [
#     ('llama3-70b-solution.jsonl', 'clean/llama3-70b-solution-clean.jsonl'),
#     ('gpt-4-turbo-2024-04-09-solution.jsonl', 'clean/gpt-4-turbo-2024-04-09-solution-clean.jsonl'),
#     ('gpt-4-1106-preview-solution.jsonl', 'clean/gpt-4-1106-preview-solution-clean.jsonl'),
#     ('gpt-4-0613-solution.jsonl', 'clean/gpt-4-0613-solution-clean.jsonl'),
#     ('gpt-4-0125-preview-solution.jsonl', 'clean/gpt-4-0125-preview-solution-clean.jsonl'),
#     ('gpt-3.5-turbo-0125-solution.jsonl', 'clean/gpt-3.5-turbo-0125-solution-clean.jsonl'),
#     ('dbrx-instruct-solution.jsonl', 'clean/dbrx-instruct-solution-clean.jsonl')
# ]

# # Function to extract answers from jsonl files
# def extract_answers(input_file, output_file):
#     with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
#         for line in infile:
#             data = json.loads(line)
#             problem_id = next(iter(data))  # Retains the original problem identifier
#             content = data[problem_id]
            
#             # Use regular expression to extract the answer part
#             match = re.search(r'"answer":\s*(.*?)(?=,\s*"reasoning")', content, re.DOTALL)
            
#             if match:
#                 answer = match.group(1).strip()
#                 answer = answer.replace('\\', '\\\\')
#                 try:
#                     if answer.startswith('"') and answer.endswith('"'):
#                         answer = json.loads(answer)
#                 except json.JSONDecodeError as e:
#                     print(f"Failed to parse JSON due to: {e}")
#                     answer = "Invalid JSON format."
#             else:
#                 answer = "No answer provided."
            
#             output_json = json.dumps({problem_id: {"answer": answer}})
#             outfile.write(output_json + '\n')

# # Process each file
# for input_path, output_path in file_paths:
#     extract_answers(input_path, output_path)