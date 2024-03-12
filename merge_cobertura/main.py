import bs4
import sys
import time
import copy

from .coverage_source import CoverageSource
from .coverage_stats import CoverageStats


def main(argv: list[str]):
    sources: list[CoverageSource] = []

    for report_path in argv[1:]:
        with open(report_path, "rt", encoding="utf-8") as report_file:
            sources.append(CoverageSource(report_file.read()))

    branches_total = CoverageStats(0, 0)
    lines_total = CoverageStats(0, 0)

    for source in sources:
        branches_total += source.branch_stats
        lines_total += source.line_stats

    soup = bs4.BeautifulSoup(features="xml")

    soup.append(
        bs4.Doctype(
            'coverage SYSTEM "http://cobertura.sourceforge.net/xml/coverage-04.dtd"'
        )
    )

    coverage = soup.new_tag(
        "coverage",
        attrs={
            "branch-rate": branches_total.rate,
            "branches-covered": branches_total.covered,
            "branches-valid": branches_total.valid,
            "line-rate": lines_total.rate,
            "lines-covered": lines_total.covered,
            "lines-valid": lines_total.valid,
            "timestamp": int(time.time()),
        },
    )

    sources_tag = soup.new_tag("sources")
    packages_tag = soup.new_tag("packages")

    for source in sources:
        source_tag = soup.new_tag("source")
        source_tag.append(source.source)
        sources_tag.append(source_tag)

        for package in source.packages.children:
            packages_tag.append(copy.copy(package))

    coverage.append(sources_tag)
    coverage.append(packages_tag)

    soup.append(coverage)

    print(soup)


def cli():
    # starts from scripts entry point
    main(sys.argv)


if __name__ == "__main__":
    main(sys.argv)
