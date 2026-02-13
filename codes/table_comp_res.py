import os
import pandas as pd

# Path to the folder containing .res files
data_folder = r'C:\pycodes\Git\FIRe_tools\data\example'

# List .res files
files = [f for f in os.listdir(data_folder) if f.lower().endswith('.res')]

data = []
header = None

for file in files:
    path = os.path.join(data_folder, file)
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        # Detect header
        for i, line in enumerate(lines):
            if 'File' in line and 'DATE' in line:
                header = line.split()
                start_idx = i + 2  # skip separator
                break
        # Read data lines
        for line in lines[start_idx:]:
            if line.strip() == '' or line.startswith('-'):
                continue
            values = line.split()
            if len(values) < len(header):
                continue
            data.append(values)

# Create DataFrame
if data and header:
    df = pd.DataFrame(data, columns=header)
    output_path = r'C:\pycodes\Git\FIRe_tools\output\compiled_res.csv'
    df.to_csv(output_path, index=False)
    print(f'Compiled table saved at: {output_path}')
else:
    print('No data found or header missing.')
