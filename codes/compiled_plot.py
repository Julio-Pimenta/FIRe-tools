import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
import numpy as np
import re
import os

def sanitize_filename(name):
    return re.sub(r'[\\/:"*?<>|]', '_', name)

output_dir = r'C:\pycodes\Git\FIRe_tools\output\plots_by_point'

# Read compiled CSV file

df = pd.read_csv(r'C:\pycodes\Git\FIRe_tools\output\compiled.csv')
# Remove rows where the file name contains "cd"
df = df[~df['File'].str.contains('cd', case=False, na=False)]

df['base'] = df['File'].str.extract(r'([^.]+)')
df['suffix'] = df['File'].str.extract(r'\.(\d{3})').astype(float)
df_filtered = df[(df['suffix'] >= 0) & (df['suffix'] <= 10)]

bases = df_filtered['base'].unique()
x_pos = {base: i*2 for i, base in enumerate(bases)}

categorical = ['File', 'DATE', 'TIME', 'base']
numeric_vars = [col for col in df_filtered.columns if col not in categorical]

vmin_color = 0.000
vmax_color = 10.000

for var in numeric_vars:
    try:
        data = df_filtered[var].astype(float)
    except Exception:
        continue

    mean = np.nanmedian(data)
    std = np.nanstd(data)
    ymin = np.nanmin(data) - 0.25*std
    ymax = np.nanmax(data) + std

    fig, ax = plt.subplots(figsize=(len(bases)*0.5, 6))
    sc = ax.scatter(
        [x_pos[base] for base in df_filtered['base']],
        data,
        c=df_filtered['suffix'],
        cmap='viridis',
        vmin=vmin_color,
        vmax=vmax_color
    )
    ax.set_xticks(list(x_pos.values()))
    ax.set_xticklabels(list(x_pos.keys()), rotation=90, ha='right')
    ax.set_xlabel('Measurement point')
    ax.set_ylabel(var)
    ax.set_ylim(ymin, ymax)
    ax.set_title(f'{var} by measurement point')
    sm = ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=vmin_color, vmax=vmax_color))
    sm.set_array([])
    plt.colorbar(sm, ax=ax, label='Suffix (.000 to .010)')
    plt.tight_layout()
    filename = os.path.join(output_dir, f'plot_{sanitize_filename(var)}.png')
    plt.savefig(filename, dpi=200)
    plt.close()

