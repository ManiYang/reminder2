"""
Provides access to database tables.
"""

import sqlite3
import os.path

_conn = None


def _get_connection():
    """
    Return the connection, establishing one if none exists.
    """
    global _conn
    if _conn is None:
        db_file = 'data/db.sqlite'
        assert os.path.isfile(db_file)
        _conn = sqlite3.connect(db_file)
    return _conn


def _check_table_exists(table):
    """
    Check that `table` exists. If not, raise an exception.
    """
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table,))
    if cursor.fetchone() is None:
        raise RuntimeError('Table "{}" does not exist.'.format(table))


def add_record(table: str, column_value: dict):
    """
    Add a record to the table.

    Args:
        table: Table name
        column_value: A dictionary (column: value)

    Returns:
        If the table has "id" column, returns the ID of the newly added record.
        Otherwise, returns None.
    """
    _check_table_exists(table)

    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM {} LIMIT 1;".format(table))
    has_id_column = 'id' in (t[0] for t in cursor.description)

    new_id = None
    if has_id_column:
        cursor.execute("SELECT MAX(id) FROM {};".format(table))
        r = cursor.fetchone()
        assert r is not None
        if r[0] is not None:
            new_id = r[0] + 1
        else:
            new_id = 1

    columns = ','.join(column_value.keys())
    placeholders = ','.join(['?'] * len(column_value))
    values = list(column_value.values())
    if has_id_column:
        columns = 'id,' + columns
        placeholders = '?,' + placeholders
        values = [new_id] + values
    try:
        cursor.execute("INSERT INTO {} ({}) VALUES ({});".format(table, columns, placeholders),
                       values)
    except sqlite3.IntegrityError as e:
        raise sqlite3.IntegrityError('Inserting into table "{}" with record {}.'
                                     .format(table, column_value)) from e
    conn.commit()

    return new_id


def query_where_equal(table, columns, column_value=None, limit=None):
    """
    Query the table with WHERE condition.

    Args:
        table (str): Table name.
        columns (list): Column names to be queried (cannot be empty).
        column_value: If given, must be a dictionary (column: value) to be used as WHERE
                      condition.
        limit: If given, will be the LIMIT of the query.

    Returns:
        (list) Query result, as a list of records, each element of which is a tuple of
        values corresponding to the specified columns.
    """
    _check_table_exists(table)

    conn = _get_connection()
    cursor = conn.cursor()
    columns_query = ','.join(columns)
    parameters = []
    if column_value is None or len(column_value) == 0:
        sql = "SELECT {} FROM {}".format(columns_query, table)
    else:
        sql = "SELECT {} FROM {} WHERE".format(columns_query, table)
        for i, c in enumerate(column_value.keys()):
            if i > 0:
                sql += " AND"
            sql += " {}=?".format(c)
        parameters.extend(column_value.values())

    if limit is not None:
        sql += " LIMIT ?"
        parameters.append(limit)

    cursor.execute(sql, parameters)
    return cursor.fetchall()

