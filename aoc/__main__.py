import os
from dataclasses import dataclass
from datetime import datetime
from itertools import product
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Template

START_YEAR = 2015
END_YEAR = datetime.now().year + 1
AOC_PATH = Path(__file__).parent


@dataclass
class TemplateFile:
    name: str
    template: Template


def _create_year_folders():
    for year in range(START_YEAR, END_YEAR):
        os.makedirs(AOC_PATH.parent.joinpath(str(year)).resolve(), exist_ok=True)


def _get_template_files() -> list[TemplateFile]:
    template_path = AOC_PATH.joinpath("templates").resolve()
    env = Environment(loader=FileSystemLoader(template_path))
    return [TemplateFile(name=str(file), template=env.get_template(str(file))) for file in os.listdir(template_path)]


def _create_files(path: Path, content: str):
    try:
        with path.open("x") as file:
            file.write(content)
    except FileExistsError:
        pass


def main():
    _create_year_folders()
    template_files = _get_template_files()
    for year, day, file in product(range(START_YEAR, END_YEAR), range(1, 26), template_files):
        year, day = str(year), str(day).zfill(2)
        file_name = file.name.format(day=day).removesuffix(".jinja")
        file_path = AOC_PATH.parent.joinpath(year).joinpath(file_name).resolve()
        content = file.template.render(year=year, day=day)
        _create_files(path=file_path, content=content)


if __name__ == "__main__":
    main()
