import csv
import json
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).parent
RAW_FILE = BASE_DIR / "raw_annotations.csv"
DISAGREEMENTS_LOG = BASE_DIR / "disagreements.log"
OUTPUT_FILE = BASE_DIR / "clean_training_dataset.jsonl"
CONFIDENCE_THRESHOLD = 0.8

def read_annotations(path):
    annotations = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                confidence = float(row["confidence_score"])
            except ValueError:
                continue
            annotations.append({
                "text": row["text"],
                "annotator_id": row["annotator_id"],
                "label": row["label"],
                "confidence": confidence,
            })
    return annotations

def find_disagreements(all_annotations):
    label_sets = defaultdict(set)
    for ann in all_annotations:
        label_sets[ann["text"]].add(ann["label"])
    return {text: labels for text, labels in label_sets.items() if len(labels) > 1}

def write_disagreements(disagreements):
    with DISAGREEMENTS_LOG.open("w", encoding="utf-8") as log_file:
        if not disagreements:
            log_file.write("No disagreements found after checks.\n")
            return
        for text, labels in disagreements.items():
            label_list = ", ".join(sorted(labels))
            log_file.write(f"Text: {text} | Labels: {label_list}\n")

def build_clean_dataset(high_conf_annotations, disagreements):
    best_by_text = {}
    for ann in high_conf_annotations:
        text = ann["text"]
        if text in disagreements:
            continue
        current = best_by_text.get(text)
        if current is None or ann["confidence"] > current["confidence"]:
            best_by_text[text] = ann
    return best_by_text.values()

def write_jsonl(records):
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        for rec in records:
            payload = {"text": rec["text"], "label": rec["label"]}
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")

def main():
    annotations = read_annotations(RAW_FILE)
    disagreements = find_disagreements(annotations)
    high_conf = [a for a in annotations if a["confidence"] >= CONFIDENCE_THRESHOLD]
    write_disagreements(disagreements)
    clean_records = build_clean_dataset(high_conf, disagreements)
    write_jsonl(clean_records)
    print(f"Annotations read: {len(annotations)}")
    print(f"High-confidence kept: {len(high_conf)}")
    print(f"Disagreements logged: {len(disagreements)}")
    print(f"Wrote clean dataset to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
