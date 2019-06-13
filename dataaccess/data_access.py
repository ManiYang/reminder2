"""
Provides functionality for adding/updating/removing/reading
reminders/categories
"""

import dataaccess._db_access as db

_TABLE_CATEGORY = 'category'
_TABLE_REMINDER = 'reminder'
_TABLE_SCENE = 'scene'
_TABLE_OCCASION = 'occasion'


def add_category(category: str):
    """
    Add new category to database.

    Args:
        category: Category name.

    Returns:
        int: ID of the newly added category.
    """
    cat_id = db.add_record(_TABLE_CATEGORY, {'name': category})
    assert cat_id is not None
    return cat_id


def add_scene(scene: str):
    """
    Add new scene to database.

    Args:
        scene: Scene name.

    Returns:
        int: ID of the newly added scene.
    """
    scene_id = db.add_record(_TABLE_SCENE, {'name': scene})
    assert scene_id is not None
    return scene_id


def add_occasion(occasion: str):
    """
    Add new occasion to database.

    Args:
        occasion: Occasion name.

    Returns:
        int: ID of the newly added occasion.
    """
    occ_id = db.add_record(_TABLE_OCCASION, {'name': occasion})
    assert occ_id is not None
    return occ_id


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


def rename_scene(old_name: str, new_name: str):
    """
    Args:
        old_name: Original name of the scene to be renamed.
        new_name: New name.
    """
    scene_id = get_scene_id(old_name)
    assert scene_id is not None, 'Scene "{}" not found.'.format(old_name)
    db.update_record(_TABLE_SCENE, {'id': scene_id, 'name': new_name})


def rename_occasion(old_name: str, new_name: str):
    """
    Args:
        old_name: Original name of the occasion to be renamed.
        new_name: New name.
    """
    occ_id = get_occasion_id(old_name)
    assert occ_id is not None, 'Occasion "{}" not found.'.format(old_name)
    db.update_record(_TABLE_OCCASION, {'id': occ_id, 'name': new_name})


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


# def remove_scene(scene: str):
#     """
#     Args:
#         scene: Name of scene to be removed. This scene cannot be involved in any reminder.
#     """
#     scene_id = get_scene_id(scene)
#     assert scene_id is not None, 'Scene "{}" not found.'.format(scene)
    # rems = db.query_where_equal(_TABLE_REMINDER, ['id'], {'category_id': cat_id})
    # assert len(rems) == 0, 'Category "{}" is associated to a reminder.'.format(category)
    # db.delete_record(_TABLE_CATEGORY, cat_id)


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


def get_scene_id(scene: str):
    """
    Args:
        scene: Scene name.

    Returns:
        int: ID of the scene, or None if the scene is not found.
    """
    r = db.query_where_equal(_TABLE_SCENE, ['id'], column_value={'name': scene}, limit=1)
    if len(r) > 0:
        return r[0][0]
    else:
        return None


def get_occasion_id(occasion: str):
    """
    Args:
        occasion: Occasion name.

    Returns:
        int: ID of the occasion, or None if the occasion is not found.
    """
    r = db.query_where_equal(_TABLE_OCCASION, ['id'], column_value={'name': occasion}, limit=1)
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


def read_scene_table():
    """
    Read whole "scene" table.

    Returns:
        A pandas DataFrame.
    """
    return db.read_table(_TABLE_SCENE).set_index('id')


def read_occasion_table():
    """
    Read whole "occasion" table.

    Returns:
        A pandas DataFrame.
    """
    return db.read_table(_TABLE_OCCASION).set_index('id')
