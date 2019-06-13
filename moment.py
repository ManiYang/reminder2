from hrmin import HrMin


class Moment:
    """
    A Moment can be of one of the types:
      + a scene
      + an HrMin
      + start of an occasion
      + end of an occasion
    Use the class methods to get an Moment instance of specific type.
    """

    TYPE_SCENE = 'scene'
    TYPE_HRMIN = 'HrMin'
    TYPE_OCCASION_START = 'occasion start'
    TYPE_OCCASION_END = 'occasion end'

    def __init__(self):
        """
        Creates an "empty" object.
        You can use the class methods to get an instance of specific type.
        Only the relevant attribute will/should be set, leaving the other 3 as None.
        """
        self.scene_id = None
        self.hrmin = None
        self.start_of_occasion_id = None
        self.end_of_occasion_id = None

    @classmethod
    def scene_moment(cls, scene_id: int):
        m = cls()
        m.scene_id = scene_id
        return m

    @classmethod
    def hrmin_moment(cls, hr=None, mn=None, hrmin=None):
        """
        Args:
            hr (int): 0 - 47
            mn (int): 0 - 59
            hrmin (HrMin): an HrMin object
        """
        assert (hr is None and mn is None) or hrmin is None
        m = cls()
        if hr:
            m.hrmin = HrMin(hr, mn)
        elif hrmin:
            m.hrmin = hrmin
        else:
            raise ValueError('Either (`hr`, `mn`) or `hrmin` should be given.')
        return m

    @classmethod
    def occasion_start_moment(cls, occasion_id: int):
        m = cls()
        m.start_of_occasion_id = occasion_id
        return m

    @classmethod
    def occasion_end_moment(cls, occasion_id: int):
        m = cls()
        m.end_of_occasion_id = occasion_id
        return m

    @property
    def type(self):
        """
        Returns:
            None if the object is not set.
        """
        if self.scene_id:
            return Moment.TYPE_SCENE
        elif self.hrmin:
            return Moment.TYPE_HRMIN
        elif self.start_of_occasion_id:
            return Moment.TYPE_OCCASION_START
        elif self.end_of_occasion_id:
            return Moment.TYPE_OCCASION_END
        else:
            return None

    def __str__(self):
        if self.scene_id:
            return 'scene {}'.format(self.scene_id)
        elif self.hrmin:
            return str(self.hrmin)
        elif self.start_of_occasion_id:
            return 'occasion {} start'.format(self.start_of_occasion_id)
        elif self.end_of_occasion_id:
            return 'occasion {} end'.format(self.end_of_occasion_id)
        else:
            return 'none'

    def __repr__(self):
        return str(self)
