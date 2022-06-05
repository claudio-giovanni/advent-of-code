import os
import re
from dataclasses import dataclass, field

import imgkit
import requests
from jinja2 import Environment, FileSystemLoader

from aoc.__main__ import AOC_FOLDER_PATH


@dataclass
class AocYear:
    year: int
    stars: int
    token: str = field(repr=False)
    _details_url: str = field(default="https://adventofcode.com/{}/leaderboard/self", init=False, repr=False)

    def __post_init__(self):
        self._auth = {"session": self.token}
        self.summary = self._get_aoc_days()

    def _get_aoc_days(self) -> dict[int, int]:
        base_days = {day: 0 for day in range(1, 26)}
        if self.stars == 0:
            return base_days
        if self.stars == 50:
            return {day: 2 for day in base_days.items()}
        details_url = self._details_url.format(self.year)
        summary_detail_response = requests.get(details_url, cookies=self._auth)
        summary_detail = re.findall(r"^\s{1,2}(\d+)(?:.*(-))?", summary_detail_response.text, re.MULTILINE)
        for day, star_flag in summary_detail:
            base_days[int(day)] = int(star_flag == "-") or 2
        return base_days


@dataclass
class Aoc:
    token: str = field(repr=False)
    _summary_url: str = field(default="https://adventofcode.com/events", init=False, repr=False)

    def __post_init__(self):
        self._auth = {"session": self.token}

    def get_summary(self) -> list[AocYear]:
        summary_response = requests.get(self._summary_url, cookies=self._auth)
        summary_response.raise_for_status()
        years_summary = re.findall(r">\[(\d{4})](?:[^\d\n\r]*(\d+))?", summary_response.text, re.MULTILINE)
        summary = []
        for year_summary in years_summary:
            year = int(year_summary[0])
            stars = int(year_summary[1] or 0)
            summary.append(AocYear(year=year, stars=stars, token=self.token))
        return summary

    def export_aoc_image(self, summary: list[AocYear]):
        html = self._get_aoc_html(summary=summary)
        image = self._convert_aoc_html_to_image(html=html)

    @staticmethod
    def _get_aoc_html(summary: list[AocYear]) -> str:
        template_path = AOC_FOLDER_PATH.joinpath("templates", "image").resolve()
        env = Environment(loader=FileSystemLoader(template_path))
        template = env.get_template("index.html")
        return template.render(aoc_years=summary, static_path=AOC_FOLDER_PATH.joinpath("templates", "static"))

    @staticmethod
    def _convert_aoc_html_to_image(html: str):
        options = {
            "enable-local-file-access": None,
            "width": 780,
        }
        imgkit.from_string(html, AOC_FOLDER_PATH.joinpath("summary.jpg"), options=options)

    def _upload_aoc_image(self, s3_path: str):
        pass


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    aoc_session = os.getenv("AOC_SESSION")
    aoc = Aoc(token=aoc_session)
    aoc_summary = aoc.get_summary()
    aoc.export_aoc_image(summary=aoc_summary)
