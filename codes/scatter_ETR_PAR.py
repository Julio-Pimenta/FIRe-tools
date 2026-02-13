import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.cm import get_cmap

# Path to compiled CSV file
csv_path = r'C:\pycodes\Git\FIRe_tools\output\compiled_res.csv'

# Read the CSV
try:
    df = pd.read_csv(csv_path)
except Exception as e:
    print(f'Error reading CSV: {e}')
    exit()

# Convert columns to float
for col in ['PAR', 'ETR']:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Remove missing values
if 'PAR' in df.columns and 'ETR' in df.columns and 'File' in df.columns:
    df = df.dropna(subset=['PAR', 'ETR', 'File'])
    # Extract prefix from file name
    df['prefix'] = df['File'].apply(lambda x: str(x).split('.')[0])
    groups = df['prefix'].unique()
    cmap = get_cmap('tab20', len(groups))
    plt.figure(figsize=(10, 7))
    for i, group in enumerate(groups):
        group_data = df[df['prefix'] == group].sort_values('PAR')
        color = cmap(i)
        plt.scatter(group_data['PAR'], group_data['ETR'], color=color, label=group, alpha=0.7)
        plt.plot(group_data['PAR'], group_data['ETR'], color=color, linewidth=2)
    plt.xlabel('PAR')
    plt.ylabel('ETR')
    plt.title('Scatterplot ETR vs PAR')
    plt.legend(title='Point', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    output_dir = r'C:\pycodes\Git\FIRe_tools\output\plots'
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'scatter_ETR_PAR.png'), dpi=200)
    plt.close()
    print(f'Plot saved at {output_dir}/scatter_ETR_PAR.png')
else:
    print('Columns PAR, ETR, or File not found in the CSV.')

