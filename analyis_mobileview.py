import json
import os
import random
from statistics import mean

DATASET_FOLDER = r"C:\Users\Jeen\Desktop\mobileview"
SAMPLE_SIZE = 100


def find_json_files(folder):
    files = []
    for root, _, filenames in os.walk(folder):
        for f in filenames:
            if f.endswith(".json"):
                files.append(os.path.join(root, f))
    return files


def has_label(node):
    text = node.get("text")
    desc = node.get("content_description")  # NOTE: different name

    return bool((text not in [None, ""]) or (desc not in [None, ""]))


def main():
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

    print("\n===== RESULTS =====")
    print(f"Avg total elements: {mean(totals):.2f}")
    print(f"Avg clickable: {mean(clickable_list):.2f}")
    print(f"Avg unlabeled: {mean(unlabeled_list):.2f}")
    print(f"Avg clickable unlabeled: {mean(clickable_unlabeled_list):.2f}")

    print(f"\nUnlabeled %: {(mean(unlabeled_list)/mean(totals))*100:.2f}%")
    print(f"Clickable unlabeled %: {(mean(clickable_unlabeled_list)/mean(clickable_list))*100:.2f}%")


if __name__ == "__main__":
    main()