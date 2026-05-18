import os
import json
import random
import pandas as pd

# =====================================
# SETTINGS
# =====================================
base_path = r"C:\Users\Jeen\Downloads\rico_dataset_v0.1_semantic_annotations\semantic_annotations"
sample_size = 100
random.seed(42)

# =====================================
# HELPER FUNCTIONS
# =====================================

def is_text_element(node):
    text_keywords = [
        "text", "edittext", "button", "checkbox",
        "radiobutton", "switch", "tab", "label"
    ]
    values = []
    for key in ["class", "text", "resource-id", "content-desc"]:
        if key in node and isinstance(node[key], str):
            values.append(node[key].lower())
    combined = " ".join(values)
    return any(keyword in combined for keyword in text_keywords)


def is_image_element(node):
    image_keywords = ["image", "icon", "img", "drawable", "avatar", "thumbnail"]
    values = []
    for key in ["class", "resource-id", "content-desc"]:
        if key in node and isinstance(node[key], str):
            values.append(node[key].lower())
    combined = " ".join(values)
    return any(keyword in combined for keyword in image_keywords)


def has_label(node):
    text = node.get("text")
    desc = node.get("content-desc")
    return bool((text not in [None, ""]) or (desc not in [None, ""]))


def get_children(node):
    return node.get("children", []) if isinstance(node.get("children"), list) else []


def traverse(node, depth=1):
    total = 1
    text_count = 1 if is_text_element(node) else 0
    image_count = 1 if is_image_element(node) else 0
    clickable_count = 1 if node.get("clickable") is True else 0
    unlabeled_count = 0 if has_label(node) else 1
    clickable_unlabeled_count = 1 if (node.get("clickable") is True and not has_label(node)) else 0
    max_depth = depth

    for child in get_children(node):
        t, tx, im, cl, ul, cul, md = traverse(child, depth + 1)
        total += t
        text_count += tx
        image_count += im
        clickable_count += cl
        unlabeled_count += ul
        clickable_unlabeled_count += cul
        max_depth = max(max_depth, md)

    return total, text_count, image_count, clickable_count, unlabeled_count, clickable_unlabeled_count, max_depth


# =====================================
# STEP 1: FIND ALL JSON FILES
# =====================================
json_files = []

for root, dirs, files in os.walk(base_path):
    for f in files:
        if f.lower().endswith(".json"):
            json_files.append(os.path.join(root, f))

print(f"Total JSON files found: {len(json_files)}")

if len(json_files) == 0:
    print("No JSON files found. Check your folder path.")
    raise SystemExit

print("\nFirst 5 JSON files found:")
for f in json_files[:5]:
    print(f)

# =====================================
# STEP 2: SAMPLE FILES SAFELY
# =====================================
sample_size = min(sample_size, len(json_files))
sample_files = random.sample(json_files, sample_size)

print(f"\nSample size used: {sample_size}")

# =====================================
# STEP 3: DEBUG ONE SAMPLE NODE
# =====================================
test_file = sample_files[0]

print("\n=== DEBUG: SAMPLE ROOT NODE ===")
print("File:", test_file)

with open(test_file, "r", encoding="utf-8") as f:
    debug_data = json.load(f)

debug_node = debug_data

print("\nRaw node keys:")
print(list(debug_node.keys()))

print("\nImportant fields:")
print("class:", debug_node.get("class"))
print("text:", debug_node.get("text"))
print("resource-id:", debug_node.get("resource-id"))
print("content-desc:", debug_node.get("content-desc"))
print("clickable:", debug_node.get("clickable"))
print("has_label:", has_label(debug_node))

print("\n=== CLASSIFICATION OF ROOT NODE ===")
print("Is TEXT element?:", is_text_element(debug_node))
print("Is IMAGE element?:", is_image_element(debug_node))
print("Is CLICKABLE?:", debug_node.get("clickable") is True)

debug_children = get_children(debug_node)
print("Children count:", len(debug_children))

if len(debug_children) > 0:
    first_child = debug_children[0]
    print("\n--- First child example ---")
    print("class:", first_child.get("class"))
    print("text:", first_child.get("text"))
    print("resource-id:", first_child.get("resource-id"))
    print("content-desc:", first_child.get("content-desc"))
    print("clickable:", first_child.get("clickable"))
    print("has_label:", has_label(first_child))
    print("Is TEXT element?:", is_text_element(first_child))
    print("Is IMAGE element?:", is_image_element(first_child))
    print("Is CLICKABLE?:", first_child.get("clickable") is True)

# =====================================
# STEP 4: ANALYZE EACH FILE
# =====================================
results = []

for file in sample_files:
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        root_node = data

        total, text_count, image_count, clickable_count, unlabeled_count, clickable_unlabeled_count, max_depth = traverse(root_node)

        results.append({
            "file": os.path.basename(file),
            "total_ui_elements": total,
            "text_elements": text_count,
            "icon_image_elements": image_count,
            "clickable_elements": clickable_count,
            "unlabeled_elements": unlabeled_count,
            "clickable_unlabeled": clickable_unlabeled_count,
            "max_tree_depth": max_depth,
            "root_direct_children": len(get_children(root_node))
        })

    except Exception as e:
        print(f"Error in {file}: {e}")

if len(results) == 0:
    print("No files were successfully analyzed.")
    raise SystemExit

# =====================================
# STEP 5: CREATE DATAFRAME
# =====================================
df = pd.DataFrame(results)

# =====================================
# STEP 6: SUMMARY TABLE
# =====================================
summary = pd.DataFrame({
    "Metric": [
        "Total UI elements",
        "Text elements",
        "Icon/Image elements",
        "Clickable elements",
        "Unlabeled elements",
        "Clickable unlabeled elements",
        "Maximum tree depth",
        "Root direct children"
    ],
    "Mean": [
        round(df["total_ui_elements"].mean(), 2),
        round(df["text_elements"].mean(), 2),
        round(df["icon_image_elements"].mean(), 2),
        round(df["clickable_elements"].mean(), 2),
        round(df["unlabeled_elements"].mean(), 2),
        round(df["clickable_unlabeled"].mean(), 2),
        round(df["max_tree_depth"].mean(), 2),
        round(df["root_direct_children"].mean(), 2),
    ],
    "Min": [
        int(df["total_ui_elements"].min()),
        int(df["text_elements"].min()),
        int(df["icon_image_elements"].min()),
        int(df["clickable_elements"].min()),
        int(df["unlabeled_elements"].min()),
        int(df["clickable_unlabeled"].min()),
        int(df["max_tree_depth"].min()),
        int(df["root_direct_children"].min()),
    ],
    "Max": [
        int(df["total_ui_elements"].max()),
        int(df["text_elements"].max()),
        int(df["icon_image_elements"].max()),
        int(df["clickable_elements"].max()),
        int(df["unlabeled_elements"].max()),
        int(df["clickable_unlabeled"].max()),
        int(df["max_tree_depth"].max()),
        int(df["root_direct_children"].max()),
    ]
})

# =====================================
# STEP 7: LEAST / MOST COMPLEX
# =====================================
least = df.loc[df["total_ui_elements"].idxmin()]
most = df.loc[df["total_ui_elements"].idxmax()]

extremes = pd.DataFrame([
    {
        "Screen": "Least complex",
        "File name": least["file"],
        "Total elements": int(least["total_ui_elements"]),
        "Unlabeled elements": int(least["unlabeled_elements"]),
        "Clickable unlabeled": int(least["clickable_unlabeled"]),
        "Max depth": int(least["max_tree_depth"]),
        "Clickable elements": int(least["clickable_elements"])
    },
    {
        "Screen": "Most complex",
        "File name": most["file"],
        "Total elements": int(most["total_ui_elements"]),
        "Unlabeled elements": int(most["unlabeled_elements"]),
        "Clickable unlabeled": int(most["clickable_unlabeled"]),
        "Max depth": int(most["max_tree_depth"]),
        "Clickable elements": int(most["clickable_elements"])
    }
])

# =====================================
# STEP 8: ACCESSIBILITY METRICS
# =====================================
avg_total = df["total_ui_elements"].mean()
avg_clickable = df["clickable_elements"].mean()
avg_unlabeled = df["unlabeled_elements"].mean()
avg_clickable_unlabeled = df["clickable_unlabeled"].mean()

unlabeled_pct = (avg_unlabeled / avg_total) * 100 if avg_total > 0 else 0
clickable_unlabeled_pct = (avg_clickable_unlabeled / avg_clickable) * 100 if avg_clickable > 0 else 0

# =====================================
# STEP 9: PRINT OUTPUT
# =====================================
print("\n=== SUMMARY TABLE ===")
print(summary.to_string(index=False))

print("\n=== LEAST / MOST COMPLEX SCREENS ===")
print(extremes.to_string(index=False))

print("\n=== ACCESSIBILITY METRICS ===")
print(f"Average unlabeled elements per screen: {avg_unlabeled:.2f}")
print(f"Average clickable unlabeled elements per screen: {avg_clickable_unlabeled:.2f}")
print(f"Avg unlabeled %: {unlabeled_pct:.2f}%")
print(f"Avg clickable unlabeled %: {clickable_unlabeled_pct:.2f}%")

print("\n=== PRESENTATION-READY POINTS ===")
print("- Higher UI complexity increases cognitive load because users must process more elements at once.")
print("- Dense interfaces make navigation harder by reducing visual clarity and scanability.")
print("- A high proportion of unlabeled elements suggests many UI components are not accessible to assistive technologies.")
print("- A high proportion of clickable unlabeled elements suggests users may struggle to understand important actions.")

# =====================================
# STEP 10: SAVE RESULTS
# =====================================
summary_output = r"C:\Users\Jeen\Desktop\summary.csv"
extremes_output = r"C:\Users\Jeen\Desktop\extremes.csv"
full_output = r"C:\Users\Jeen\Desktop\sampled_ui_metrics.csv"

summary.to_csv(summary_output, index=False)
extremes.to_csv(extremes_output, index=False)
df.to_csv(full_output, index=False)

print("\nSaved files:")
print(summary_output)
print(extremes_output)
print(full_output)