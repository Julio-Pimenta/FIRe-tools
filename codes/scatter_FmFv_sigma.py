import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import os
from sklearn.metrics import r2_score

def sanitize_filename(name):
    return re.sub(r'[\\/:"*?<>|]', '_', name)

output_dir = r'C:\pycodes\Git\FIRe_tools\output\plots_first'

df = pd.read_csv(r'C:\pycodes\Git\FIRe_tools\output\compiled.csv')
df = df[~df['File'].str.contains('cd', case=False, na=False)]
df['group'] = df['File'].str[:3]
df['suffix'] = df['File'].str.extract(r'\.(\d{3})').astype(float)
df_filtered = df[df['suffix'] == 0.0]

def best_fit(X, y):
    # Linear
    coef_lin = np.polyfit(X, y, 1)
    y_pred_lin = np.polyval(coef_lin, X)
    r2_lin = r2_score(y, y_pred_lin)
    # 2nd degree polynomial
    coef_poly2 = np.polyfit(X, y, 2)
    y_pred_poly2 = np.polyval(coef_poly2, X)
    r2_poly2 = r2_score(y, y_pred_poly2)
    # Exponential
    try:
        popt = np.polyfit(X, np.log(y), 1)
        y_pred_exp = np.exp(np.polyval(popt, X))
        r2_exp = r2_score(y, y_pred_exp)
    except Exception:
        r2_exp = -np.inf
    fits = {
        'Linear': (y_pred_lin, r2_lin, lambda x: np.polyval(coef_lin, x)),
        '2nd degree': (y_pred_poly2, r2_poly2, lambda x: np.polyval(coef_poly2, x)),
        'Exponential': (y_pred_exp if r2_exp != -np.inf else None, r2_exp, lambda x: np.exp(np.polyval(popt, x)) if r2_exp != -np.inf else None)
    }
    best_name = max(fits, key=lambda k: fits[k][1])
    _, best_r2, best_func = fits[best_name]
    return best_name, best_r2, best_func

groups = sorted(df_filtered['group'].unique())
cmap = plt.get_cmap('tab20')
colors = {g: cmap(i % 20) for i, g in enumerate(groups)}

fig, axs = plt.subplots(2, 1, figsize=(8, 12))

# --- FvD/FmD ---
df_plot = df_filtered[['FvD/FmD', 'Sigma', 'group']].dropna()
df_plot['FvD/FmD'] = df_plot['FvD/FmD'].astype(float)
df_plot['Sigma'] = df_plot['Sigma'].astype(float)
X = df_plot['Sigma'].values
y = df_plot['FvD/FmD'].values
name, r2, func = best_fit(X, y)
for g in groups:
    data = df_plot[df_plot['group'] == g]
    axs[0].scatter(data['Sigma'], data['FvD/FmD'], color=colors[g], edgecolor='k', alpha=0.7, label=g)
x_fit = np.linspace(X.min(), X.max(), 200)
axs[0].plot(x_fit, func(x_fit), color='black', lw=2, label=f'{name} (R²={r2:.2f})')
axs[0].set_xlabel('Sigma')
axs[0].set_ylabel('FvD/FmD')
axs[0].set_title('FvD/FmD vs Sigma (.000)')
axs[0].legend(title='Reservoir', bbox_to_anchor=(1.05, 1), loc='upper left')

# --- Fv/Fm ---
df_plot2 = df_filtered[['Fv/Fm', 'Sigma', 'group']].dropna()
df_plot2['Fv/Fm'] = df_plot2['Fv/Fm'].astype(float)
df_plot2['Sigma'] = df_plot2['Sigma'].astype(float)
X2 = df_plot2['Sigma'].values
y2 = df_plot2['Fv/Fm'].values
name2, r2_2, func2 = best_fit(X2, y2)
for g in groups:
    data = df_plot2[df_plot2['group'] == g]
    axs[1].scatter(data['Sigma'], data['Fv/Fm'], color=colors[g], edgecolor='k', alpha=0.7, label=g)
x_fit2 = np.linspace(X2.min(), X2.max(), 200)
axs[1].plot(x_fit2, func2(x_fit2), color='black', lw=2, label=f'{name2}  (R²={r2_2:.2f})')
axs[1].set_xlabel('Sigma')
axs[1].set_ylabel('Fv/Fm')
axs[1].set_title('Fv/Fm vs Sigma (.000)')
axs[1].legend(title='Reservoir', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
filename = os.path.join(output_dir, 'scatter_FvDFmD_FvFm_vs_Sigma_000_reg.png')
plt.savefig(filename, dpi=200)
plt.close()

