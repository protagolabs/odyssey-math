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
    file_pred = "/Users/elricwan/Downloads/NetmindAI/odyssey-math/jsonl/clean/deepseek-v3-Instruct-solution-clean.jsonl"
    results = process_files(file_true, file_pred)
    save_jsonl(results, 'jsonl/eval/result-'+file_pred.split('/')[-1])
    print("Results have been saved.")

if __name__ == "__main__":
    main()
