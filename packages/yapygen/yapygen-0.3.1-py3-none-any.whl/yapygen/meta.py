import re
from dataclasses import dataclass, field
from enum import StrEnum

from InquirerPy.base.control import Choice
from InquirerPy.prompts.input import InputPrompt
from InquirerPy.prompts.list import ListPrompt


class PyVersion(StrEnum):
    PY38 = "3.8"
    PY39 = "3.9"
    PY310 = "3.10"
    PY311 = "3.11"
    PY312 = "3.12"


class License(StrEnum):
    NONE = ""
    MIT = "MIT"

    @property
    def filename(self) -> str:
        return "LICENSE"

    @property
    def name(self) -> str:
        match self:
            case License.MIT:
                return "MIT License"
            case License.NONE:
                return "create project without license"


@dataclass
class ProjectInfo:
    name: str
    description: str
    minimum_python: PyVersion
    license: License
    author_name: str
    author_email: str
    package: str
    license_str: str = field(init=False)

    def __post_init__(self):
        self.license_str = (
            ""
            if self.license == License.NONE
            else f'\nlicense = {{ file = "{self.license.filename}" }}'
        )


name = InputPrompt(
    message="Project name:",
    default="demo",
    validate=lambda x: re.match(
        r"^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$", x, re.IGNORECASE
    )
    is not None,
    transformer=lambda x: re.sub(r"[-_.]+", "-", x).lower(),
    filter=lambda x: re.sub(r"[-_.]+", "-", x).lower(),
    long_instruction=" A valid name consists only of "
    "ASCII letters and numbers, "
    "period, underscore and hyphen. "
    "It must start and end with a letter or number.",
)

description = InputPrompt(
    message="Project description:", default="a simple python project"
)

min_py = ListPrompt(
    message="Minimum python version:",
    choices=[version for version in PyVersion],
    default=PyVersion.PY310,
)

license = ListPrompt(
    message="License:",
    choices=[Choice(license, name=license.name) for license in License],
)

author_name = InputPrompt(message="Author name:", default="Author Placeholder")

author_email = InputPrompt(message="Author email:", default="email@placeholder.com")

package = InputPrompt(
    message="Top level package name:",
    default="demo",
    validate=lambda x: re.match(r"^([A-Z]|[A-Z][A-Z_]*[A-Z])$", x, re.IGNORECASE)
    is not None,
)


def get_info() -> ProjectInfo:
    return ProjectInfo(
        name=name.execute(),
        description=description.execute(),
        minimum_python=min_py.execute(),
        license=license.execute(),
        author_name=author_name.execute(),
        author_email=author_email.execute(),
        package=package.execute(),
    )
