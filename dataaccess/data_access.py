"""
Provides functionality for adding/reading/updating/removing
reminders/categories/...
"""

import dataaccess._db_access as db

_TABLE_CATEGORY = 'category'
_TABLE_REMINDER = 'reminder'


def add_category(category: str):
    """
    Add the category to database.

    Args:
        category: Category name.

    Returns:
        int: ID of the newly added category.
    """
    cat_id = db.add_record(_TABLE_CATEGORY, {'name': category})
    assert cat_id is not None
    return cat_id


def get_category_id(category: str):
    """
    Args:
        category: Category name.

    Returns:
        int: ID of the category, or None if the category is not found.
    """
    r = db.query_where_equal(_TABLE_CATEGORY, ['id'], column_value={'name': category}, limit=1)
    if len(r) > 0:
        return r[0][0]
    else:
        return None


def add_reminder(reminder):
    """
    Add the reminder to database. The newly created reminder ID will be assign to
    attribute reminder.id.

    Args:
        reminder: A Reminder object.
    """
    assert reminder.id is None
    rem_id = db.add_record(_TABLE_REMINDER, reminder.field_value_dict)
    assert rem_id is not None
    reminder.id = rem_id
