from moment import Moment
from period import Period
import json


class ActTimeModel:
    """
    ActTimeModel controls when a reminder is active. It can be of one of the types:
      + "moments": Showing up at moments, closed by user.
      + "periods": Shown during periods (closed when period ends).
      + "moments during periods": Showing up at moments during periods, closed by user.

    Attributes:
        moments: For "moments" type: a list of Moment's.
        periods: For "periods" type: a list of Period's.
        moments_periods: For "moments during periods" type:
            [ ( Moment,       Period), ...,
              ((start, step), Period), ... ]
            A list of (moments, period) tuples, where moments can be a list of Moments, or a
            tuple (start, step) of int.
    """

    TYPE_MOMENTS = "moments"
    TYPE_PERIODS = "periods"
    TYPE_MOMENTS_DURING_PERIODS = "moments during periods"

    def __init__(self):
        self.moments = []
        self.periods = []
        self.moments_periods = []

    @classmethod
    def moments_model(cls, moments):
        """
        Args:
            moments: A list of Moment's.
        """
        assert isinstance(moments, list)
        assert all(isinstance(m, Moment) for m in moments)
        a = cls()
        a.moments = moments
        return a

    @classmethod
    def periods_model(cls, periods):
        """
        Args:
            periods: A list of Period's.
        """
        assert isinstance(periods, list)
        assert all(isinstance(p, Period) for p in periods)
        a = cls()
        a.periods = periods
        return a

    @classmethod
    def moments_during_periods_model(cls, moments_periods):
        """
        Args:
            moments_periods: [ ( Moment,       Period), ...,
                               ((start, step), Period), ... ]
        """
        assert isinstance(moments_periods, list)
        for mp in moments_periods:
            assert isinstance(mp, tuple)
            assert len(mp) == 2
            assert isinstance(mp[1], Period)

            assert isinstance(mp[0], (Moment, tuple))
            if isinstance(mp[0], tuple):
                assert len(mp[0]) == 2
                assert isinstance(mp[0][0], int) and isinstance(mp[0][1], int)
        a = cls()
        a.moments_periods = moments_periods
        return a

    @property
    def type(self):
        """
        Returns:
            None if the object is not set.
        """
        if self.moments:
            return ActTimeModel.TYPE_MOMENTS
        elif self.periods:
            return ActTimeModel.TYPE_PERIODS
        elif self.moments_periods:
            return ActTimeModel.TYPE_MOMENTS_DURING_PERIODS
        else:
            return None

    def to_json(self):
        if self.moments:
            return json.dumps({ActTimeModel.TYPE_MOMENTS: self.moments},
                              default=lambda x: str(x))
        elif self.periods:
            return json.dumps({ActTimeModel.TYPE_PERIODS: self.periods},
                              default=lambda x: str(x))
        elif self.moments_periods:
            mps = [{'mo': mo, 'pe': pe} for mo, pe in self.moments_periods]
            return json.dumps({ActTimeModel.TYPE_MOMENTS_DURING_PERIODS: mps},
                              default=lambda x: str(x))
        else:
            return json.dumps(None)
