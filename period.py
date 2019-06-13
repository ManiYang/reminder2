from hrmin import HrMin
from moment import Moment


class Period:
    """
    A Period can be
      + a time interval, defined by a starting HrMin and a time span
      + an occasion
      + a scene extended by a time span
      + a start/end of occasion extended by a time span
    Use the class methods to get an instance of specific type.

    Attributes:
        start_moment (Moment): The start moment.
        span (HrMin): Time span. None if the Period is an occasion.
    """

    TYPE_TIME_INTERVAL = 'time interval'
    TYPE_SCENE_EXTENDED = 'scene extended'
    TYPE_OCCASION = 'occasion'
    TYPE_OCCASION_START_EXTENDED = 'occasion start extended'
    TYPE_OCCASION_END_EXTENDED = 'occasion end extended'

    def __init__(self):
        self.start_moment = None
        self.span = None

    @classmethod
    def hrmin_interval_period(cls, start_hrmin, end_hrmin=None, span_hrmin=None):
        """
        Args:
            start_hrmin (HrMin): Start time.
            end_hrmin (HrMin): End time.
            span_hrmin (HrMin): Time span.
                                (Only 1 of end_hrmin, span_hrmin should be given.)
        """
        assert end_hrmin is None or span_hrmin is None, \
            'Only 1 of the arguments `end_hrmin`, `span_hrmin` can be given.'

        span = None
        if end_hrmin:
            assert start_hrmin < end_hrmin
            span = HrMin.from_minutes(end_hrmin - start_hrmin)
        elif span_hrmin:
            assert start_hrmin + span_hrmin < 2880
            span = span_hrmin
        else:
            raise ValueError('Either `end_hrmin` or `span_hrmin` should be given.')

        p = cls()
        p.start_moment = Moment.hrmin_moment(hrmin=start_hrmin)
        p.span = span
        return p

    @classmethod
    def occasion_period(cls, occasion_id: int):
        p = cls()
        p.start_moment = Moment.occasion_start_moment(occasion_id)
        p.span = None
        return p

    @classmethod
    def scene_extended_period(cls, scene_id: int, span: HrMin):
        p = cls()
        p.start_moment = Moment.scene_moment(scene_id)
        p.span = span
        return p

    @classmethod
    def occasion_start_extended_period(cls, occasion_id: int, span: HrMin):
        p = cls()
        p.start_moment = Moment.occasion_start_moment(occasion_id)
        p.span = span
        return p

    @classmethod
    def occasion_end_extended_period(cls, occasion_id: int, span: HrMin):
        p = cls()
        p.start_moment = Moment.occasion_end_moment(occasion_id)
        p.span = span
        return p

    @property
    def type(self):
        """
        Returns:
            None if the object is not set.
        """
        if self.start_moment.type == Moment.TYPE_HRMIN:
            return Period.TYPE_TIME_INTERVAL
        elif self.start_moment.type == Moment.TYPE_SCENE:
            return Period.TYPE_SCENE_EXTENDED
        elif self.start_moment.type == Moment.TYPE_OCCASION_START:
            if self.span is None:
                return Period.TYPE_OCCASION
            else:
                return Period.TYPE_OCCASION_START_EXTENDED
        elif self.start_moment.type == Moment.TYPE_OCCASION_END:
            return Period.TYPE_OCCASION_END_EXTENDED
        else:
            return None

    def __str__(self):
        if self.start_moment is None:
            return 'none'

        assert self.start_moment.type is not None
        if self.start_moment.type == Moment.TYPE_OCCASION_START and self.span is None:
            return 'occasion {}'.format(self.start_moment.start_of_occasion_id)

        assert self.span is not None
        return 'since {} for {}'.format(self.start_moment, self.span)
