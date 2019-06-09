"""
Provides functionality for adding/updating/removing/reading
reminders/categories
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


def add_reminder(reminder):
    """
    Add the reminder to database. The newly created reminder ID will be assign to
    attribute reminder.id.

    Args:
        reminder: A Reminder object.
    """
    assert reminder.id is None
    field_values = reminder.to_dict(exclude_id=True)
    rem_id = db.add_record(_TABLE_REMINDER, field_values)
    assert rem_id is not None
    reminder.id = rem_id


def rename_category(old_name: str, new_name: str):
    """
    Args:
        old_name: Original name of the category to be renamed.
        new_name: New name.
    """
    cat_id = get_category_id(old_name)
    assert cat_id is not None, 'Category "{}" not found.'.format(old_name)
    db.update_record(_TABLE_CATEGORY, {'id': cat_id, 'name': new_name})


def update_reminder(reminder):
    """
    Updates the reminder, overwriting the reminder data with the same ID in the database.

    Args:
        reminder: A Reminder object.
    """
    assert reminder.id is not None
    field_values = reminder.to_dict(exclude_id=False)
    db.update_record(_TABLE_REMINDER, field_values)


def remove_category(category: str):
    """
    Args:
        category: Name of category to be removed. This category cannot be associated to
                  any reminder.
    """
    cat_id = get_category_id(category)
    assert cat_id is not None, 'Category "{}" not found.'.format(category)
    rems = db.query_where_equal(_TABLE_REMINDER, ['id'], {'category_id': cat_id})
    assert len(rems) == 0, 'Category "{}" is associated to a reminder.'.format(category)
    db.delete_record(_TABLE_CATEGORY, cat_id)


def remove_reminder(reminder_id: int):
    """
    Args:
        reminder_id: ID of reminder to be removed.
    """
    db.delete_record(_TABLE_REMINDER, reminder_id)


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


def read_category_table():
    """
    Read whole "category" table.

    Returns:
        A pandas DataFrame.
    """
    return db.read_table(_TABLE_CATEGORY).set_index('id')


def read_reminder_table():
    """
    Read whole "reminder" table.

    Returns:
        A pandas DataFrame.
    """
    return db.read_table(_TABLE_REMINDER).set_index('id')


