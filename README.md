# Text Annotation Pipeline PoC

This folder shows a small slice of the system design: the Quality Validator & Output Generator for annotated text.

## Files
- `design_document.md` — high-level architecture and choices.
- `raw_annotations.csv` — sample labels from multiple annotators.
- `process_annotations.py` — filters low-confidence rows, logs disagreements, and writes a clean JSONL dataset.
- `disagreements.log` — disagreement report created by the script.
- `clean_training_dataset.jsonl` — final training data created by the script.

## How to run
1. Use Python 3.9+ (a venv is already set up here /Users/usmanaziz/textannotation/venv). From this folder run:
   ```bash
   python3 process_annotations.py
   ```
2. Outputs land in the same folder: `disagreements.log` and `clean_training_dataset.jsonl`.

## What the script does
- Drops any annotation with confidence < 0.8.
- Flags texts that received different labels from annotators (logged to `disagreements.log`).
- Emits one JSONL line per agreed text using the highest-confidence label.

## Assumption

This architecture is a simple depiction of the solution and I have used Copilot in creating this solution. We can enhance the application by adding several layers and Lambdas. e.g. We can add a data store for integrity using a DB so that we can track and ensure the integrity of the metadata. Moreover, we can add more components and layers e.g. Using Lambda with docker images, Using Glue jobs to transfer raw data after transformation to the DB, We can add deployment pipeline using GitHub Actions with additional linting and test layer.
