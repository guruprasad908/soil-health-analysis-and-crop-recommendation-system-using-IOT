import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

# Create output directory
OUTPUT_DIR = "report_graphs"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print(f"Generating graphs for your report in '{OUTPUT_DIR}' folder...")

def create_factors_chart(filename):
    """Generates a Bar Chart of All Project Factors (Suitability Score)"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Factors used in the project
    factors = [
        'Nitrogen (N)', 'Phosphorus (P)', 'Potassium (K)', 
        'Soil pH', 'Soil Moisture', 
        'Temperature', 'Humidity', 'Rainfall'
    ]
    
    # Simulated Suitability Scores (0-100) for the report
    scores = [85, 60, 90, 95, 45, 88, 75, 80]
    
    # Raw values for annotation
    raw_values = [
        "85 mg/kg", "24 mg/kg", "160 mg/kg", 
        "6.5 pH", "35 %", 
        "26 °C", "62 %", "800 mm"
    ]
    
    # Colors based on score
    colors = ['#2ecc71' if s >= 75 else '#f39c12' if s >= 50 else '#e74c3c' for s in scores]
    
    y_pos = np.arange(len(factors))
    
    # Horizontal Bar Chart
    bars = ax.barh(y_pos, scores, color=colors, height=0.6, edgecolor='black', alpha=0.8)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(factors, fontsize=11, fontweight='bold')
    ax.invert_yaxis()  # Labels read top-to-bottom
    ax.set_xlabel('Suitability Score (0-100)', fontsize=11, fontweight='bold')
    ax.set_title('Environmental & Soil Factors Analysis', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(0, 110)
    
    # Add Score and Raw Value Labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        # Score Label inside/outside bar
        ax.text(width + 1, bar.get_y() + bar.get_height()/2, 
                f"{scores[i]}/100", 
                va='center', fontweight='bold', fontsize=10)
        
        # Raw Value annotation
        ax.text(10, bar.get_y() + bar.get_height()/2, 
                f"Value: {raw_values[i]}", 
                va='center', color='white', fontweight='bold', fontsize=9,
                bbox=dict(facecolor='black', alpha=0.3, edgecolor='none', boxstyle='round,pad=0.2'))

    # Legend for status
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#2ecc71', edgecolor='black', label='Good (>75)'),
        Patch(facecolor='#f39c12', edgecolor='black', label='Moderate (50-75)'),
        Patch(facecolor='#e74c3c', edgecolor='black', label='Poor (<50)')
    ]
    ax.legend(handles=legend_elements, loc='lower right')
    
    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Created {filename}")

def create_model_comparison(filename):
    """Generates Model Accuracy Bar Chart"""
    models = ['Random Forest', 'XGBoost', 'SVM', 'Decision Tree']
    accuracy = [98.5, 96.2, 92.0, 89.5] # Example values based on project
    
    plt.figure(figsize=(8, 5))
    bars = plt.bar(models, accuracy, color=['#2ecc71', '#3498db', '#95a5a6', '#95a5a6'])
    
    plt.ylim(80, 100)
    plt.ylabel('Accuracy (%)', fontsize=11)
    plt.title('Crop Prediction Model Performance', fontsize=14, fontweight='bold')
    
    # Add values on top
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height}%', ha='center', va='bottom', fontweight='bold')
                
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    
    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Created {filename}")

def create_npk_chart(filename):
    """Generates NPK vs Ideal Chart"""
    nutrients = ['Nitrogen', 'Phosphorus', 'Potassium']
    current_values = [45, 22, 180] # Example: High K
    ideal_values = [100, 50, 50]   # Ideal baseline
    
    x = np.arange(len(nutrients))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(8, 5))
    rects1 = ax.bar(x - width/2, current_values, width, label='Current Soil', color='#e74c3c')
    rects2 = ax.bar(x + width/2, ideal_values, width, label='Ideal Requirement', color='#2ecc71')
    
    ax.set_ylabel('Nutrient Level (mg/kg)')
    ax.set_title('Nutrient Deficiency Analysis', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(nutrients)
    ax.legend()
    
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    
    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Created {filename}")

# --- Execute Generation ---
if __name__ == "__main__":
    create_factors_chart("project_factors_analysis.png")
    create_model_comparison("model_accuracy_comparison.png")
    create_npk_chart("npk_analysis_chart.png")
    
    print("\n🎉 DONE! All graphs are saved in the 'report_graphs' folder.")
