"""
Provides access to database tables.
"""

from sqlalchemy import create_engine
import pandas as pd
import sqlite3
import os.path

_DB_FILE = 'data/db.sqlite'
_sqlite_conn = None
_sqlalchemy_engine = None
# Use sqlite3 and sqlalchemy simultaneously. Will this cause any problem?


def _get_sqlite_connection():
    """
    Returns the connection, establishing one if none exists.
    """
    global _sqlite_conn
    if _sqlite_conn is None:
        assert os.path.isfile(_DB_FILE)
        _sqlite_conn = sqlite3.connect(_DB_FILE)
    return _sqlite_conn


def _get_sqlalchemy_engine():
    """
    Returns the engine, establishing one if none exists.
    """
    global _sqlalchemy_engine
    if _sqlalchemy_engine is None:
        assert os.path.isfile(_DB_FILE)
        _sqlalchemy_engine = create_engine('sqlite:///' + _DB_FILE)
    return _sqlalchemy_engine


def _check_table_exists(table):
    """
    Check that `table` exists. If not, raise an exception.
    """
    conn = _get_sqlite_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table,))
    if cursor.fetchone() is None:
        raise RuntimeError('Table "{}" does not exist.'.format(table))


def add_record(table: str, column_value: dict):
    """
    Add a record to the table.

    Args:
        table: Table name
        column_value: A dictionary (column: value), without 'id' key.

    Returns:
        If the table has "id" column, returns the ID of the newly added record.
        Otherwise, returns None.
    """
    _check_table_exists(table)

    conn = _get_sqlite_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM {} LIMIT 1;".format(table))
    has_id_column = 'id' in (t[0] for t in cursor.description)

    assert 'id' not in column_value
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


def update_record(table: str, column_value: dict):
    """
    Update a record in the table. The table must have a 'id' field.
    The record with the id equal to that given in `column_value` gets updated.

    Args:
        table: Table name.
        column_value: A dictionary of column-value pairs. Must include 'id' key.
    """
    assert 'id' in column_value
    _check_table_exists(table)

    conn = _get_sqlite_connection()
    cursor = conn.cursor()
    sql = ("UPDATE {} SET "
           + ','.join([col + '=?' for col in column_value.keys() if col != 'id'])
           + " WHERE id=?;").format(table)
    parameters = [v for col, v in column_value.items() if col != 'id'] + [column_value['id']]
    cursor.execute(sql, parameters)
    conn.commit()


def delete_record(table: str, record_id: int):
    """
    Delete the record with id = `record_id` from the table `table`.
    Args:
        table: Table name. The table must have an "id" column.
        record_id: ID of the record to be deleted.
    """
    _check_table_exists(table)

    conn = _get_sqlite_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM {} WHERE id=?".format(table), (record_id,))
    conn.commit()


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

    conn = _get_sqlite_connection()
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


def read_table(table: str):
    """
    Read a whole table.

    Args:
        table: Table name.
        
    Returns:
        A pandas DataFrame.
    """
    engine = _get_sqlalchemy_engine()
    df = pd.read_sql_query("SELECT * FROM {};".format(table), engine)
    return df
