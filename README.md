# Audim

Animation engine for audio-based and voice-based podcast videos.

## Prerequisites

- Python ≥ 3.10
- Conda

## Setup

### 1. Clone the repository:

```bash
git clone https://github.com/mratanusarkar/audim.git
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

### 3. Code Quality

Before committing, please ensure that the code is formatted and styled correctly.
Run the following commands to check and fix code style issues:

```bash
# Check and fix code style issues
ruff format .
ruff check --fix .
```
