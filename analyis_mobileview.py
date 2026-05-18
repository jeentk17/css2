import json
import os
import random
import csv
from statistics import mean

DATASET_FOLDER = r"C:\Users\Jeen\Desktop\mobileview"
OUTPUT_FOLDER = r"C:\Users\Jeen\Desktop\css2_allfile"
SAMPLE_SIZE = 100

random.seed(42)


def find_json_files(folder):
    files = []
    for root, _, filenames in os.walk(folder):
        for f in filenames:
            if f.endswith(".json"):
                files.append(os.path.join(root, f))
    return files


def has_label(node):
    text = node.get("text")
    desc = node.get("content_description")

    return bool((text not in [None, ""]) or (desc not in [None, ""]))


def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    print("Finding JSON files...")
    files = find_json_files(DATASET_FOLDER)
    print(f"Total JSON found: {len(files)}")

    sample = random.sample(files, min(SAMPLE_SIZE, len(files)))

    totals = []
    clickable_list = []
    unlabeled_list = []
    clickable_unlabeled_list = []

    for i, path in enumerate(sample):
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)

            views = data.get("views", [])

            total = len(views)
            clickable = 0
            unlabeled = 0
            clickable_unlabeled = 0

            for node in views:
                click = node.get("clickable", False)
                label = has_label(node)

                if click:
                    clickable += 1

                if not label:
                    unlabeled += 1
                    if click:
                        clickable_unlabeled += 1

            totals.append(total)
            clickable_list.append(clickable)
            unlabeled_list.append(unlabeled)
            clickable_unlabeled_list.append(clickable_unlabeled)

        except Exception as e:
            print(f"Error in {path}: {e}")
            continue

        if i % 10 == 0:
            print(f"Processed {i}/{len(sample)}")

    avg_total = mean(totals)
    avg_clickable = mean(clickable_list)
    avg_unlabeled = mean(unlabeled_list)
    avg_clickable_unlabeled = mean(clickable_unlabeled_list)

    unlabeled_percent = (avg_unlabeled / avg_total) * 100
    clickable_unlabeled_percent = (avg_clickable_unlabeled / avg_clickable) * 100

    result_text = f"""
===== MOBILEVIEWS RESULTS =====
Total JSON found: {len(files)}
Sample size: {len(sample)}

Avg total elements: {avg_total:.2f}
Avg clickable: {avg_clickable:.2f}
Avg unlabeled: {avg_unlabeled:.2f}
Avg clickable unlabeled: {avg_clickable_unlabeled:.2f}

Unlabeled %: {unlabeled_percent:.2f}%
Clickable unlabeled %: {clickable_unlabeled_percent:.2f}%
"""

    print(result_text)

    txt_path = os.path.join(OUTPUT_FOLDER, "mobileview_results.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(result_text)

    csv_path = os.path.join(OUTPUT_FOLDER, "mobileview_results.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "Value"])
        writer.writerow(["Total JSON found", len(files)])
        writer.writerow(["Sample size", len(sample)])
        writer.writerow(["Avg total elements", f"{avg_total:.2f}"])
        writer.writerow(["Avg clickable", f"{avg_clickable:.2f}"])
        writer.writerow(["Avg unlabeled", f"{avg_unlabeled:.2f}"])
        writer.writerow(["Avg clickable unlabeled", f"{avg_clickable_unlabeled:.2f}"])
        writer.writerow(["Unlabeled %", f"{unlabeled_percent:.2f}%"])
        writer.writerow(["Clickable unlabeled %", f"{clickable_unlabeled_percent:.2f}%"])

    print(f"Saved TXT to: {txt_path}")
    print(f"Saved CSV to: {csv_path}")


if __name__ == "__main__":
    main()