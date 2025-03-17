# Development

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

Run with:

```bash
python run.py
```

## Build and serve the documentation

You can build and serve the documentation by running:

```bash
uv pip install -e .[docs]
mkdocs serve
```
