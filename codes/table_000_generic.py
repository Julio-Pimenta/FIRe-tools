import os
import pandas as pd

# Path to the folder containing .RES files
data_folder = r'C:\pycodes\Git\FIRe_tools\data\example'

# List .RES files
files = [f for f in os.listdir(data_folder) if f.lower().endswith('.res')]

data = []

for file in files:
    path = os.path.join(data_folder, file)
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        # Find header
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
            # Only keep lines where File ends with .000
            if values[0].lower().endswith('.000'):
                data.append(values)

# Create DataFrame
if data:
    df = pd.DataFrame(data, columns=header)
    output_path = r'C:\pycodes\Git\FIRe_tools\output\compiled_000.csv'
    df.to_csv(output_path, index=False)
    print(f'Compiled table saved at: {output_path}')
else:
    print('No .000 data found.')

