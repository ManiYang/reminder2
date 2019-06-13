
class HrMin:
    """
    Attributes:
        hr (int): hour, can be 0 - 47
        mn (int): minute, can be 0 - 59
    """

    def __init__(self, hr: int, mn: int):
        """
        Args:
            hr: 0 - 47
            mn: 0 - 59
        """
        assert 0 <= hr <= 47
        assert 0 <= mn <= 59
        self.hr = hr
        self.mn = mn

    @classmethod
    def from_minutes(cls, minutes: int):
        """
        Args:
            minutes: 0 - 2879
        """
        assert 0 <= minutes <= 2879
        return cls(minutes // 60, minutes % 60)

    @property
    def hour(self):
        return self.hr

    @property
    def minute(self):
        return self.mn

    def to_minutes(self):
        return self.hr * 60 + self.mn

    def __lt__(self, other):
        return (self.hr, self.mn) < (other.hr, other.mn)

    def __add__(self, other) -> int:
        """
        Args:
            other: can be an HrMin or int (representing minutes)

        Returns:
             Minutes.
        """
        if isinstance(other, HrMin):
            return self.to_minutes() + other.to_minutes()
        elif isinstance(other, int):
            return self.to_minutes() + other
        else:
            raise TypeError('Invalid type of `other`')

    def __sub__(self, other) -> int:
        """
        Args:
            other: An HrMin.
        Returns:
            The difference (self - other), in minutes.
        """
        return (self.hr - other.hr) * 60 + (self.mn - other.mn)

    @staticmethod
    def _normalize(hr: int, mn: int):
        """
        Returns:
            The resulting (hr, mn).
        """
        return hr + mn // 60, mn % 60

    def __str__(self):
        return '{:02d}:{:02d}'.format(self.hr, self.minute)

