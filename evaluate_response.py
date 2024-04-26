import json
from agents.evaluate import Evalutor

def load_jsonl(filename):
    """Load JSONL file and return a list of dictionaries."""
    with open(filename, 'r') as file:
        return [json.loads(line) for line in file]

def save_jsonl(data, filename):
    """Save a list of dictionaries to a JSONL file."""
    with open(filename, 'w') as file:
        for entry in data:
            file.write(json.dumps(entry) + '\n')

def process_files(file_true, file_pred):
    """Process files to compare true and predicted answers and save results."""
    true_answers = load_jsonl(file_true)
    predicted_answers = load_jsonl(file_pred)
    evalution = Evalutor()

    results = []
    for true, pred in zip(true_answers, predicted_answers):
        problem_id = list(true.keys())[0]
        true_info = true[problem_id]
        
        # Check if pred[problem_id] is a string or needs JSON parsing
        if isinstance(pred[problem_id], str):
            try:
                # Try to parse it as JSON in case it's a JSON string inline
                pred_data = json.loads(pred[problem_id])
                pred_answer = pred_data["answer"] if "answer" in pred_data else pred[problem_id]
            except json.JSONDecodeError:
                # If it's not a JSON string, use it directly
                pred_answer = 'No answer provided.'
        else:
            # Assume it's a dictionary with an "answer" key
            pred_answer = pred[problem_id]["answer"]

        comparison_result = evalution(question=true_info["question"], true=true_info["answer"], prediction=pred_answer)

        result_data = {
            problem_id: {
                "true": true_info["answer"],
                "prediction": pred_answer,
                "is_correct": comparison_result,
                "label": true_info["label"],
                "level": true_info["level"],  
            }
        }
        results.append(result_data)

    return results

def main():
    file_true = 'final-odyssey-math-with-levels.jsonl'
    file_pred = 'jsonl/gpt-4-0125-preview-solution.jsonl'
    results = process_files(file_true, file_pred)
    save_jsonl(results, 'jsonl/evaluation_results.jsonl')
    print("Results have been saved to 'evaluation_results.jsonl'.")

if __name__ == "__main__":
    main()
