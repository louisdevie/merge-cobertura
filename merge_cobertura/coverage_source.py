import bs4

from .coverage_stats import CoverageStats


class CoverageSource:
    __packages: bs4.Tag
    __source: str
    __branch_stats: CoverageStats
    __line_stats: CoverageStats

    def __init__(self, markup: str):
        soup = bs4.BeautifulSoup(markup, "xml")
        coverage = soup.coverage

        assert coverage is not None

        self.__branch_stats = CoverageStats(
            CoverageSource.__get_int_attribute(coverage, "branches-covered"),
            CoverageSource.__get_int_attribute(coverage, "branches-valid"),
        )
        self.__line_stats = CoverageStats(
            CoverageSource.__get_int_attribute(coverage, "lines-covered"),
            CoverageSource.__get_int_attribute(coverage, "lines-valid"),
        )

        assert coverage.source is not None
        self.__source = coverage.source.getText()

        assert coverage.packages is not None
        self.__packages = coverage.packages

    @staticmethod
    def __get_int_attribute(tag: bs4.Tag, attr: str) -> int:
        values = tag[attr]
        return int(values if isinstance(values, str) else values[0])

    @property
    def branch_stats(self) -> CoverageStats:
        return self.__branch_stats

    @property
    def line_stats(self) -> CoverageStats:
        return self.__line_stats

    @property
    def source(self) -> str:
        return self.__source

    @property
    def packages(self) -> bs4.Tag:
        return self.__packages
