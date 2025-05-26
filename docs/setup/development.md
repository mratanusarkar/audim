# Development

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/mratanusarkar/audim.git
cd audim
```

### 2. Install FFmpeg locally (recommended)

Using local FFmpeg is optional but recommended for speeding up the video encoding process.

!!! example "Install FFmpeg"

    === "Ubuntu"

        ```bash
        sudo apt install ffmpeg libx264-dev
        ```

    === "MacOS"

        ```bash
        brew install ffmpeg
        ```

    === "Windows"

        ```bash
        choco install ffmpeg
        ```

    === "Windows (manual)"

        Download and install FFmpeg from the official website:

        - [Download FFmpeg](https://ffmpeg.org/download.html)
        - Ensure FFmpeg is in your system PATH

    === "Other platforms"

        Download and install FFmpeg from the official website:

        - [Download FFmpeg](https://ffmpeg.org/download.html)
        - Follow the installation instructions for your platform

### 3. Setting up the project environment

We recommend using `uv` to manage your project environment since `audim` was developed using `uv`,
and you can replicate the same environment by just running:

```bash
uv sync
```

But, feel free to use any python based environment and package manager of your choice.

!!! tip "About uv"

    [uv](https://docs.astral.sh/uv/) is a fast, simple, and secure Python package manager.
    It is recommended to use `uv` to manage your project environment.

### 3.1 Installing `uv`

!!! note "Note"

    If you are using conda base environment as the default base environment for your python projects,
    run the below command to activate the base environment.
    
    If not, skip this step and continue with the next step.

    ```bash
    conda activate base
    ```

If you don't have `uv` installed, you can install it by running:

=== "Linux"

    ```bash
    # Install uv
    pip install uv

    # Setup project environment
    uv venv

    source .venv/bin/activate

    uv pip install -e ".[dev,docs]"
    ```

=== "Windows"

    ```bash
    # Install uv
    pip install uv

    # Setup project environment
    uv venv

    .venv\Scripts\activate

    uv pip install -e ".[dev,docs]"
    ```

### 4. Create input and output directories

```bash
mkdir ./input ./output
```

Create a `test.py` or `run.py` to test your python script using `audim`.

```bash
touch test.py
```

ideally, if done correctly, the setup should be like this:

```bash
audim/
├── audim/
├── docs/
├── input/
├── output/
├── README.md
└── test.py # or run.py
```

!!! tip "Note"

    - You would dump your input files in the `input` directory.
    - The output files will be dumped in the `output` directory.
    - See [Usage](../usage/index.md) for more details or see sample scripts to get some inspiration.

## Code Quality

Before committing, please ensure that the code is formatted and styled correctly.
Run the following commands to check and fix code style issues:

```bash
# Check and fix code style issues
ruff format .
ruff check --fix .
```

## Run the project

feel free to create a `run.py` or `test.py` file to test the project.
They will be untracked by git.

implement your usage logic in the `run.py` file.

Run the script with:

```bash
python run.py
```

## Build and serve the documentation

You can build and serve the documentation by running:

```bash
uv pip install -e .[docs]
mkdocs serve
```
