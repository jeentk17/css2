import matplotlib.pyplot as plt
import pandas as pd
import os

# =========================
# OUTPUT FOLDER
# =========================
OUTPUT_FOLDER = r"C:\Users\Jeen\Desktop\css2_allfile\css2_graphs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# =========================
# YOUR RESULTS
# =========================
datasets = ["RICO (2016)", "MobileViews (2024)"]

data = {
    "Dataset": datasets,
    "Avg UI Elements": [21.42, 105.93],
    "Avg Clickable Elements": [6.81, 21.23],
    "Avg Unlabeled Elements": [13.01, 72.48],
    "Avg Clickable Unlabeled": [4.86, 6.95],
    "Unlabeled %": [60.74, 68.42],
    "Clickable Unlabeled %": [71.37, 32.74],
}

df = pd.DataFrame(data)

# Save summary table
df.to_csv(os.path.join(OUTPUT_FOLDER, "css2_summary_results.csv"), index=False)


# =========================
# HELPER FUNCTION
# =========================
def save_bar_chart(column, title, ylabel, filename):
    plt.figure(figsize=(8, 5))
    bars = plt.bar(df["Dataset"], df[column])

    plt.title(title, fontsize=14, fontweight="bold")
    plt.ylabel(ylabel)
    plt.xlabel("Dataset")

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{height:.2f}",
            ha="center",
            va="bottom",
            fontsize=10
        )

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, filename), dpi=300)
    plt.close()


# =========================
# GRAPH 1: UI COMPLEXITY
# =========================
save_bar_chart(
    "Avg UI Elements",
    "Increase in UI Complexity: RICO vs MobileViews",
    "Average UI Elements per Screen",
    "graph1_ui_complexity.png"
)

# =========================
# GRAPH 2: UNLABELED %
# =========================
save_bar_chart(
    "Unlabeled %",
    "Percentage of Unlabeled UI Elements",
    "Unlabeled Elements (%)",
    "graph2_unlabeled_percentage.png"
)

# =========================
# GRAPH 3: CLICKABLE UNLABELED %
# =========================
save_bar_chart(
    "Clickable Unlabeled %",
    "Clickable but Unlabeled Elements",
    "Clickable Unlabeled Elements (%)",
    "graph3_clickable_unlabeled_percentage.png"
)

# =========================
# GRAPH 4: CLICKABLE ELEMENTS
# =========================
save_bar_chart(
    "Avg Clickable Elements",
    "Increase in Interactive Elements",
    "Average Clickable Elements per Screen",
    "graph4_clickable_elements.png"
)

# =========================
# GRAPH 5: RAW UNLABELED ELEMENTS
# =========================
save_bar_chart(
    "Avg Unlabeled Elements",
    "Average Number of Unlabeled Elements",
    "Average Unlabeled Elements per Screen",
    "graph5_unlabeled_elements.png"
)

# =========================
# GRAPH 6: GROUPED COMPARISON
# =========================
metrics = ["Avg UI Elements", "Avg Clickable Elements", "Avg Unlabeled Elements", "Avg Clickable Unlabeled"]

x = range(len(metrics))
rico_values = [df.loc[0, metric] for metric in metrics]
mobile_values = [df.loc[1, metric] for metric in metrics]

plt.figure(figsize=(11, 6))
width = 0.35

plt.bar([i - width/2 for i in x], rico_values, width, label="RICO (2016)")
plt.bar([i + width/2 for i in x], mobile_values, width, label="MobileViews (2024)")

plt.title("Raw UI Metric Comparison", fontsize=14, fontweight="bold")
plt.ylabel("Average Count per Screen")
plt.xticks(x, metrics, rotation=20, ha="right")
plt.legend()

for i, value in enumerate(rico_values):
    plt.text(i - width/2, value, f"{value:.2f}", ha="center", va="bottom", fontsize=9)

for i, value in enumerate(mobile_values):
    plt.text(i + width/2, value, f"{value:.2f}", ha="center", va="bottom", fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_FOLDER, "graph6_grouped_raw_metrics.png"), dpi=300)
plt.close()


print("DONE! Graphs saved to:")
print(OUTPUT_FOLDER)
print("\nFiles created:")
for file in os.listdir(OUTPUT_FOLDER):
    print("-", file)