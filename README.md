# FIRe tools

FIRe tools is a collection of Python codes for compiling, analyzing, and visualizing raw results acquired with the FIRE instrument used at FRRF.

## Objectives
- Compile raw results from the FIRE instrument
- Organize and standardize raw datasets
- Generate plots and visualizations
- Compute statistical metrics and summaries

## Repository Organization
- `codes/` – Source code for data compilation, analysis, and visualization
- `data/` – Raw input data from the FIRE instrument
- `output/` – Compiled datasets, figures, and statistical results

## Technologies
- Python
- NumPy / SciPy
- Matplotlib / Seaborn

## Installation
This project uses Conda for environment management. To create the environment with all dependencies, run:

```sh
conda env create -f environment.yml
conda activate FIRe_tools
```

## Usage
1. Clone the repository.
2. Install the dependencies as described above.
3. Place your raw FIRE data in the `data/` directory.
4. Run the desired script from the `codes/` directory. For example:

```sh
python codes/scatter_ETR_PAR.py
```

The output files will be generated in the `output/` directory.

## Notes
Raw data may not be included in the repository due to size or confidentiality constraints.


