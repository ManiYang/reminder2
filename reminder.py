
class Reminder:
    """
    Attributes:
        _id: The ID of the reminder in the database. It can be only set onece. It will be set
             by dataaccess.add_reminder(). Do not set it by other means.
        category_id: int or None
        content (str): Textual content of the reminder.
        up_when (str): Defines when the reminder shows up.
    """

    def __init__(self):
        self._id = None
        self.category_id = None
        self.content = ''
        self.up_when = ''

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, _id: int):
        assert self._id is None, 'ID has already been set.'
        assert _id is not None
        self._id = _id

    # def to_dict(self, exclude_id=True):
    #     """
    #     Returns:
    #         A dictionary whose keys are the fields in the database table.
    #     """
    #     field_values = {'category_id': self.category_id,
    #                     'content': self.content, 'up_when': self.up_when}
    #     if not exclude_id:
    #         field_values['id'] = self._id
    #     return field_values

    # @classmethod
    # def from_dict(cls, field_value_dict):
    #     """
    #     Args:
    #         field_value_dict: A dictionary whose keys are the fields in the database table.
    #     """
    #     rem = cls()
    #     rem._id = field_value_dict['id']
    #     rem.category_id = field_value_dict['category_id']
    #     rem.content = field_value_dict['content']
    #     rem.up_when = field_value_dict['up_when']
    #     return rem

    # def __str__(self):
    #     return 'id: {}, category_id: {}, content: "{}", up_when: "{}"' \
    #         .format(self._id, self.category_id, self.content, self.up_when)
    #
    # def __repr__(self):
    #     return 'Reminder\n  id: {}\n  category_id: {}\n  content: "{}"\n  up_when: "{}"' \
    #         .format(self._id, self.category_id, self.content, self.up_when)
