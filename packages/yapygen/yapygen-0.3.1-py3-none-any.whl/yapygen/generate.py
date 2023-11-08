import os
import shutil
import sys
from dataclasses import asdict
from datetime import datetime
from importlib.resources import files
from pathlib import Path
from string import Template

from InquirerPy.prompts.confirm import ConfirmPrompt

import yapygen
from yapygen.meta import License, ProjectInfo


def load_file(name: str) -> str:
    root = files(yapygen).joinpath("templates")
    content = root.joinpath(name).read_text(encoding="utf-8")
    return content


def load_template(name: str) -> Template:
    return Template(load_file(name))


def render(name: str, info: ProjectInfo, **kwargs: object) -> str:
    param = asdict(info)
    param.update(kwargs)
    return load_template(name).safe_substitute(param)


def setup_root(root: Path) -> None:
    if not root.exists():
        root.mkdir()
    if any(root.iterdir()):
        if ConfirmPrompt(
            message=f"Target {root.name} is not empty, remove contents:",
            default=False,
        ).execute():
            for i in root.iterdir():
                if i.is_dir():
                    shutil.rmtree(i)
                else:
                    os.remove(i)
        else:
            print("Exit without generate project.")
            sys.exit(0)


def generate_directories(info: ProjectInfo, root: Path) -> None:
    top_level_package = root / "src" / info.package
    top_level_package.mkdir(parents=True)
    (top_level_package / "__init__.py").touch()
    (top_level_package / "py.typed").touch()


def generate_files(info: ProjectInfo, root: Path) -> None:
    file_dict = {
        ".flake8": load_file(".flake8"),
        ".gitignore": load_file(".gitignore"),
        ".pre-commit-config.yaml": load_file(".pre-commit-config"),
        "MANIFEST.in": load_file("MANIFEST.in"),
        "pyproject.toml": render("pyproject", info),
        "README.md": render("README", info),
    }
    if info.license != License.NONE:
        file_dict[info.license.filename] = render(
            f"licenses/{info.license}", info, year=str(datetime.now().year)
        )
    for filename, content in file_dict.items():
        (root / filename).write_text(content, encoding="utf-8")


def main(info: ProjectInfo) -> None:
    current_dir: bool = ConfirmPrompt(
        message="Generate in current directory:", default=False
    ).execute()
    root = Path.cwd() if current_dir else Path.cwd() / info.name
    setup_root(root)
    generate_directories(info, root)
    generate_files(info, root)
