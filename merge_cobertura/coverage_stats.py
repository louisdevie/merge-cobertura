class CoverageStats:
    __covered: int
    __valid: int

    def __init__(self, covered: int, valid: int):
        self.__covered = covered
        self.__valid = valid

    def __add__(self, other):
        if isinstance(other, CoverageStats):
            return CoverageStats(
                self.__covered + other.__covered,
                self.__valid + other.__valid,
            )
        else:
            return NotImplemented

    @property
    def covered(self) -> int:
        return self.__covered

    @property
    def valid(self) -> int:
        return self.__valid

    @property
    def rate(self) -> float:
        return self.__covered / self.__valid if self.__valid > 0 else 0
