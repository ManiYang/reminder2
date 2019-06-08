
class Reminder:
    """
    Attributes:
        id: The ID of the reminder in the database. It will be given by
            dataaccess.add_reminder(). Do not set it by other means.
        category_id: int or None
        content (str): Textual content of the reminder.
        time (str): Defines when the reminder shows up.
    """
    def __init__(self):
        self.id = None
        self.category_id = None
        self.content = ''
        self.time = ''

    @property
    def field_value_dict(self):
        return {'category_id': self.category_id, 'content': self.content, 'time': self.time}
