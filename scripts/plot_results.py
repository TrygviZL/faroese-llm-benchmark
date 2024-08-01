import json
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load results from a JSON file
def load_results(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Calculate accuracy from results
def calculate_accuracy(results):
    correct_count = sum(result['is_correct'] for result in results)
    total_count = len(results)
    accuracy = correct_count / total_count * 100
    return accuracy

# Plot accuracies for each test category
def plot_accuracies(accuracies):
    categories = list(accuracies.keys())
    accuracy_values = list(accuracies.values())

    sns.set(style="whitegrid")
    plt.figure(figsize=(8, 5))
    sns.barplot(x=categories, y=accuracy_values, palette="viridis")
    plt.title("Model Accuracy by Test Category")
    plt.xlabel("Category")
    plt.ylabel("Accuracy (%)")
    plt.ylim(0, 100)

    for i, accuracy in enumerate(accuracy_values):
        plt.text(i, accuracy + 2, f'{accuracy:.2f}%', ha='center', va='bottom')

    plt.savefig('../results/accuracy_plot.png')
    plt.show()

# Main function to generate plots
def main():
    results_dir = '../results'
    test_files = {
        'grammar': 'grammar_results.json',
        'morphological': 'morphological_results.json',
        'translation': 'translation_results.json'
    }

    accuracies = {}
    for category, file_name in test_files.items():
        results_path = os.path.join(results_dir, file_name)
        results = load_results(results_path)
        accuracy = calculate_accuracy(results)
        accuracies[category] = accuracy

    plot_accuracies(accuracies)

if __name__ == "__main__":
    main()

