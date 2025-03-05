# Installation

## Prerequisites

- Python ≥ 3.10
- Conda

## Setup

### 1. Clone the repository:

```bash
git clone https://github.com/mratanusarkar/audim.git
cd audim
```

### 2. Install `uv` and setup project environment:

> **Note**: If you are using conda base environment as the default base environment for your python projects, run the below command to activate the base environment. If not, skip this step and continue with the next step.
>
> ```bash
> conda activate base
> ```

```bash
# Install uv
pip install uv

# Setup project environment
uv venv

source .venv/bin/activate   # on Linux
# .venv\Scripts\activate    # on Windows

uv pip install -e ".[dev,docs]"
```

### 3. Create input and output directories:

```bash
mkdir ./input ./output
```

ideally, if done correctly, the setup should be like this:

```bash
audim/
├── audim/
├── docs/
├── input/
├── output/
└── README.md
```

Note: you would dump your input files in the `input` directory and the output files will be dumped in the `output` directory.
