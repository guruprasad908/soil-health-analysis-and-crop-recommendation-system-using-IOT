import matplotlib.pyplot as plt
import numpy as np
import os

# User provided data
models = [
    "Decision Tree", "Random Forest", "Gradient Boosting",
    "SVM", "KNN", "Logistic Regression", "Stacking Classifier"
]

accuracy = [98.86, 99.55, 98.64, 96.59, 95.91, 97.50, 99.55]
precision = [98.71, 99.42, 98.49, 96.38, 95.67, 97.32, 99.42]
recall = [98.68, 99.38, 98.46, 96.35, 95.64, 97.29, 99.38]
f1_score = [98.70, 99.40, 98.48, 96.37, 95.66, 97.31, 99.40]

x = np.arange(len(models))
width = 0.2

plt.figure(figsize=(14, 7))
plt.bar(x - 1.5*width, accuracy, width, label='Accuracy')
plt.bar(x - 0.5*width, precision, width, label='Precision')
plt.bar(x + 0.5*width, recall, width, label='Recall')
plt.bar(x + 1.5*width, f1_score, width, label='F1-Score')

plt.xlabel("Machine Learning Models")
plt.ylabel("Performance Score (%)")
plt.title("Performance Comparison of Machine Learning Models")
plt.xticks(x, models, rotation=20)
plt.ylim(94, 100)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.6)

plt.tight_layout()

# Save logic
output_dir = "report_graphs"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

filename = "model_performance_comparison.png"
output_path = os.path.join(output_dir, filename)
plt.savefig(output_path, dpi=300)
print(f"Chart saved to {output_path}")
