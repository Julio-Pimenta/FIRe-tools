# ...existing code from grafico_000_generico.py, now in English and with updated paths...
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Path to compiled CSV file
csv_path = r'C:\pycodes\Git\FIRe_tools\output\compiled_000.csv'
df = pd.read_csv(csv_path)

# Function to plot scatter, 1:1 line, regression, and save
def scatter_regression(x_col, y_col, output_name, title, x_label, y_label):
    # Convert columns to float
    for col in [x_col, y_col]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    data = df.dropna(subset=[x_col, y_col])
    x = data[x_col].values.reshape(-1, 1)
    y = data[y_col].values
    # Linear regression
    reg = LinearRegression().fit(x, y)
    y_pred = reg.predict(x)
    r2 = r2_score(y, y_pred)
    # Scatterplot
    plt.figure(figsize=(8, 6))
    plt.scatter(data[x_col], data[y_col], alpha=0.7, label='Data')
    # 1:1 line
    lims = [min(data[x_col].min(), data[y_col].min()), max(data[x_col].max(), data[y_col].max())]
    plt.plot(lims, lims, 'k--', label='1:1', alpha=0.6)
    # Regression line
    plt.plot(data[x_col], y_pred, color='red', label='Linear regression')
    # Equation and R²
    eq = f'y = {reg.coef_[0]:.3f}x + {reg.intercept_:.3f}\n$R^2$ = {r2:.3f}'
    plt.text(0.05, 0.95, eq, transform=plt.gca().transAxes, fontsize=11, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xlim(250, 400)
    plt.ylim(0, 1)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_name, dpi=200)
    plt.close()
    print(f'Plot saved at {output_name}')

# Fv/Fm vs Sigma
scatter_regression('Sigma', 'Fv/Fm', r'C:\pycodes\Git\FIRe_tools\output\plots\scatter_fvfm_sigma.png', 'Scatterplot Fv/Fm vs Sigma (.000)', 'Sigma', 'Fv/Fm')

# FvD/FmD vs Sigma
scatter_regression('Sigma', 'FvD/FmD', r'C:\pycodes\Git\FIRe_tools\output\plots\scatter_fvdfmd_sigma.png', 'Scatterplot FvD/FmD vs Sigma (.000)', 'Sigma', 'FvD/FmD')
# This file ensures the 'plots' directory is tracked by git.

