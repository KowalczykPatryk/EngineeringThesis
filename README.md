


## Running using uv

`uv init` - to initialize new project which creates a pyproject.toml, a lock file, and a starter script.

`uv add` - to add package to this project

`uv run {script.py}` - running python script inside uv environment

`uv sync` - to download all packages saved to lock file

`uv run python -m package_name.file` - to run script as package

## Running ruff

Lint code: `uv run ruff check .`  

Fix lint errors: `uv run ruff check --fix .`  

Format code: `uv run ruff format .`  
