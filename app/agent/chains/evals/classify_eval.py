import json
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from chains.email_classifier import email_classifier

DATA_PATH = Path(__file__).parent / "data" / "classify_email_cases.json"

def load_cases():
    with open(DATA_PATH) as f:
        return json.load(f)
    
def run_eval():
    cases = load_cases()
    results = []
    for case in cases:
        result = email_classifier.invoke({"subject": case["subject"], "body": case["body"]})
        correct = result.category.value == case["expected_category"]
        results.append({**case, "actual": result.category.value, "correct": correct, "reasoning": result.reasoning})

    accuracy = sum(r["correct"] for r in results) / len(results)
    print(f"Accuracy: {accuracy:.1%} ({sum(r['correct'] for r in results)}/{len(results)})")
    for r in results:
        if not r["correct"]:
            print(f"  WRONG: expected={r['expected_category']} got={r['actual']} | subject={r['subject']!r}")

if __name__ == "__main__":
    run_eval()
