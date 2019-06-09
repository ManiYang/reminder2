from reminder import Reminder


def get_reminder_from_dataframe(df_reminders, reminder_id):
    """
    Args:
        df_reminders: A pandas DataFrame of reminders.
        reminder_id: Reminder ID whose data will be extracted from `df_reminders`.

    Returns:
        A Reminder object.
    """
    if df_reminders.index.name == 'id':
        assert reminder_id in df_reminders.index, \
            'Reminder with ID {} not found in the given DataFrame.'.format(reminder_id)
        field_values = df_reminders.loc[[reminder_id]].reset_index().to_dict('records')[0]
    else:
        assert 'id' in df_reminders.columns
        record = df_reminders[df_reminders['id'] == reminder_id]
        assert len(record) != 0, \
            'Reminder with ID {} not found in the given DataFrame.'.format(reminder_id)
        field_values = record.to_dict('records')[0]
    return Reminder.from_dict(field_values)
