import json
from typing import Dict, List, Any
import os
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

# Load environment variables
load_dotenv()

class FaroeseLLMTester:
    def __init__(self):
        self.tests = self.load_tests()
        
        # Correctly load the API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")
        
        # Initialize the OpenAI client with the API key
        self.client = OpenAI(api_key=api_key)

    def load_tests(self) -> Dict[str, List[Dict[str, Any]]]:
        dirname = os.path.dirname(__file__)
        tests = {}
        
        # Define the filenames and their corresponding keys in JSON
        file_key_mapping = {
            "test_grammar_rules": "grammar_rule_application",
            "test_morphological_understanding": "morphological_understanding",
            "test_translation_accuracy": "translation_accuracy",
        }
        
        # Iterate through the file-key mapping
        for filename, key in file_key_mapping.items():
            file_path = os.path.join(dirname, f"../data/{filename}.json")
            with open(file_path, "r", encoding="utf-8") as file:
                tests[key] = json.load(file)[key]
        
        return tests

    def generate_response(self, prompt: str, system_prompt: str) -> str:
        # Generate a response using the new OpenAI API client
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content.strip()

    def save_results(self, test_type: str, results: List[Dict[str, Any]]):
        """Save the test results to a JSON file."""
        # Ensure the results directory exists
        results_dir = os.path.join(os.path.dirname(__file__), "../results")
        os.makedirs(results_dir, exist_ok=True)
        
        # Create a timestamp for the results file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{test_type}_results_{timestamp}.json"
        file_path = os.path.join(results_dir, file_name)
        
        # Write the results to a JSON file
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(results, file, ensure_ascii=False, indent=4)

    def run_morphological_understanding_test(self) -> Dict[str, float]:
        results = []
        correct = 0
        total = len(self.tests["morphological_understanding"])
        
        for question in self.tests["morphological_understanding"]:
            response = self.generate_response(
                prompt=question["question"],
                system_prompt=question["system_prompt"]
            )
            is_correct = response.lower() == question["expected_answer"].lower()
            if is_correct:
                correct += 1

            # Append detailed result for this question
            results.append({
                "question": question,
                "response": response,
                "is_correct": is_correct
            })
        
        # Save results to file
        self.save_results("morphological_understanding", results)

        accuracy = correct / total
        return {"accuracy": accuracy, "correct": correct, "total": total}

    def run_translation_accuracy_test(self) -> Dict[str, float]:
        results = []
        correct = 0
        total = len(self.tests["translation_accuracy"])
        
        for question in self.tests["translation_accuracy"]:
            if question["type"] == "Faroese to English":
                prompt = f"Translate the following Faroese sentence to English: {question['faroese']}"
            else:
                prompt = f"Translate the following English sentence to Faroese: {question['english']}"
            
            response = self.generate_response(
                prompt=prompt,
                system_prompt=question["system_prompt"]
            )
            
            is_correct = response.lower() == question["expected_answer"].lower()
            if is_correct:
                correct += 1
            
            # Append detailed result for this question
            results.append({
                "question": question,
                "response": response,
                "is_correct": is_correct
            })

        # Save results to file
        self.save_results("translation_accuracy", results)

        accuracy = correct / total
        return {"accuracy": accuracy, "correct": correct, "total": total}

    def run_grammar_rule_application_test(self) -> Dict[str, float]:
        results = []
        correct = 0
        total = len(self.tests["grammar_rule_application"])
        
        for question in self.tests["grammar_rule_application"]:
            prompt = question["question"]
            response = self.generate_response(
                prompt=prompt,
                system_prompt=question["system_prompt"]
            )
            is_correct = response.lower() == question["expected_answer"].lower()
            if is_correct:
                correct += 1

            # Append detailed result for this question
            results.append({
                "question": question,
                "response": response,
                "is_correct": is_correct
            })

        # Save results to file
        self.save_results("grammar_rule_application", results)

        accuracy = correct / total
        return {"accuracy": accuracy, "correct": correct, "total": total}

    def run_all_tests(self) -> Dict[str, Dict[str, float]]:
        results = {
            "morphological_understanding": self.run_morphological_understanding_test(),
            "translation_accuracy": self.run_translation_accuracy_test(),
            "grammar_rule_application": self.run_grammar_rule_application_test()
        }
        return results

def main():
    tester = FaroeseLLMTester()
    results = tester.run_all_tests()

    print("Test Results:")
    for test_type, result in results.items():
        print(f"{test_type.replace('_', ' ').title()}:")
        print(f"  Accuracy: {result['accuracy']:.2%}")
        print(f"  Correct: {result['correct']}/{result['total']}")
        print()

if __name__ == "__main__":
    main()

