import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_emissions_summary(csv_path="results/emissions.csv", output_dir="results"):
    
    """Reads emissions.csv and generates a visual chart image of the footprint."""
    if not os.path.exists(csv_path):
        print("⚠️ No emissions CSV found to plot yet.")
        return

    df = pd.read_csv(csv_path)
    
    # Check if data exists
    if df.empty:
        return

    plt.figure(figsize=(8, 4), dpi=300)
    
    # Plotting emissions per run index or project name
    runs = range(len(df))
    plt.bar(runs, df['emissions'], color="#10b981", width=0.5, label="Emissions (kg CO2eq)")
    
    plt.title("Carbon Footprint Tracking per Execution", fontsize=12, fontweight="bold")
    plt.xlabel("Run Index", fontsize=10)
    plt.ylabel("Emissions (kg CO2eq)", fontsize=10)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend()
    plt.tight_layout()

    chart_output = os.path.join(output_dir, "carbon_footprint_summary.png")
    plt.savefig(chart_output)
    plt.close()
    print(f"📊 Carbon footprint chart saved to {chart_output}")

# Call this at the end of your pipeline script!
if __name__ == "__main__":
    plot_emissions_summary()