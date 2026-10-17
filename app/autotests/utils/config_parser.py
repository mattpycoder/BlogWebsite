import tomllib
from pathlib import Path
from typing import Any

PYPROJECT_CONFIG_FILE = "pyproject.toml"


def parse_config_file(config_file_path: Path) -> Any:
    with config_file_path.open("rb") as config_file:
        toml_data_root = tomllib.load(config_file)
        toml_data_root_selection = toml_data_root.get("blogwebsite", {})
        return toml_data_root_selection["settings"]
