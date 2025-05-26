# Installation

!!! note "Note"

    This guide is for end users using Audim for creating podcast videos.
    For developers and contributors, see [Development](./development.md).

## Prerequisites

- 🐍 Python ≥ 3.10
- 🖥️ Conda or venv
- 🎥 FFmpeg (recommended, for faster video encoding)

## Setup

### 1. Install Audim

It is recommended to install `audim` in a virtual environment from PyPI or Conda in a [Python=3.10](https://www.python.org/) environment.

=== "Install using PyPI"

    Activate your virtual environment (recommended):

    ```bash
    source .venv/bin/activate
    ```

    Install `audim` using `pip`:

    ```bash
    pip install audim
    ```

=== "Install using Conda"

    Create a new environment using Conda:

    ```bash
    conda create -n my-project python=3.10
    ```

    Activate your virtual environment:

    ```bash
    conda activate my-project
    ```

    Install `pip` and `audim` using `conda`:

    ```bash
    conda install pip
    pip install audim
    ```

=== "Install from source"

    !!! tip "Note"

        By installing `audim` from source, you can explore the latest features and enhancements that have not yet been officially released.
    
    !!! warning "Note"

        Please note that the latest changes may be still in development and may not be stable and may contain bugs.

    Install from source

    ```bash
    pip install git+https://github.com/mratanusarkar/audim.git
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

## Start your project

Create input and output directories

```bash
mkdir ./input ./output
```

Create a `run.py` or `test.py` to write your python script using `audim` and start creating your podcast videos.

```bash
touch run.py
```

Ideally, if done correctly, the setup should look like this:

```bash
your-project/
├── .venv/
├── input/
├── output/
└── run.py # or test.py
```

Now, you are all set!

- Go ahead and create your python script in `run.py` to start creating your podcast videos.
- See [Usage](../usage/index.md) for more details or see sample scripts to get some inspiration.
- Once done, you would dump your input files in the `input` directory.
- The output files will be generated in the `output` directory on running the script.

Run the script using:

```bash
python run.py
```

Feel free to share your generations and tag us!
