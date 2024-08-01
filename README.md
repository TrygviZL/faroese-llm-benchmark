# Faroese LLM Benchmark

This repository contains a benchmark for evaluating large language models (LLMs) on Faroese grammar and translation accuracy. It includes tests for grammar rule application, morphological understanding, and translation tasks.

## Table of Contents

- [Introduction](#introduction)
- [Datasets](#datasets)
- [Setup and Installation](#setup-and-installation)
- [Running the Tests](#running-the-tests)
- [Generating Plots](#generating-plots)
- [Results](#results)

## Introduction

The Faroese LLM Benchmark is designed to assess the proficiency of language models in Faroese. This benchmark focuses on three key areas:

1. **Grammar Rule Application**: Tests the model's ability to apply grammatical rules correctly.
2. **Morphological Understanding**: Evaluates the model's understanding of morphological forms.
3. **Translation Accuracy**: Assesses the model's ability to translate between Faroese and English.

## Datasets

The datasets used for testing are located in the `data/` directory:

### 1. Grammar Rule Application

- **File**: `test_grammar_rules.json`
- **Example**:
  ```json
  {
    "type": "Fill-in-the-Blank",
    "question": "Complete the sentence: 'Eg síggi ___ (the elephant - acc.).'",
    "sentence": "Eg síggi ___ (the elephant - acc.).",
    "expected_answer": "fílin",
    "grammar_rule": "accusative definite singular"
  }
  ```

### 2. Morphological Understanding

- **File**: `test_morphological_understanding.json`
- **Example**:
  ```json
  {
    "question": "What is the accusative singular indefinite form of 'fílur'?",
    "word": "fílur",
    "expected_answer": "fíl",
    "grammatical_context": {
      "case": "accusative",
      "number": "singular",
      "definiteness": "indefinite"
    }
  }
  ```

### 3. Translation Accuracy

- **File**: `test_translation_accuracy.json`
- **Example**:
  ```
  {
    "type": "Faroese to English",
    "question": "Translate: 'Fílarnir ganga í skóginum.'",
    "faroese": "Fílarnir ganga í skóginum.",
    "expected_answer": "The elephants walk in the forest.",
    "grammar_focus": ["definite plural", "present tense"]
  }
  ```

## Setup and Installation

### Prerequisites

- Python 3.10 or later
- An OpenAI API key

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/TrygviZL/faroese-llm-benchmark
    cd Faroese-LLM-Benchmark
    ```
  

2. Install the required packages:

    ```bash
    poetry shell
    poetry install
    ```


3. Setup OpenAI API keyby adding the key to a .env file in the root of the project:

    ```bash
    OPENAI_API_KEY='your-api-key'
    ```

## Running the Tests

To run all the tests, execute the following command in your terminal:

```bash
python scripts/run_tests.py
```

## Generating plots

```bash
python scripts/generate_plots.py
```

## Results

The results are stored in the results/ directory:

* grammar_results.json: Contains the results of grammar rule application tests.
* morphological_results.json: Contains the results of morphological understanding tests.
* translation_results.json: Contains the results of translation accuracy tests.

