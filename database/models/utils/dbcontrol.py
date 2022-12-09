from typing import Dict, List, Tuple
from database.models import createdb
from config.db_config import USERS_TABLE, PROGRESS_TABLE, MESSAGES_TABLE

database = createdb.DbCreator()
conn = database.conn
cursor = database.cursor


def insert_db(table: str, column_val: Dict):
    """Insert data to DB"""
    columns = ', '.join(column_val.keys())
    values = tuple(map(str, column_val.values()))
    cursor.execute(
        f"INSERT INTO {table.lower()} "
        f"({columns}) "
        f"VALUES {values} "
        f"ON CONFLICT DO NOTHING"
    )
    conn.commit()


def update_db(table: str, row_val: Dict, column_val: Dict):
    """Updates data in db"""
    column = list(column_val.keys())[0]
    column_value = list(column_val.values())[0]
    if isinstance(column_value, str):
        column_value = "'" + column_value + "'"
    row = list(row_val.keys())
    if len(row) == 2:  # крайне плохая реализация, но рабочая в контексте одного проекта
        cursor.execute(
            f"UPDATE {table.lower()} "
            f"SET {column} = {column_value} "
            f"WHERE {row[0]} = {row_val.get(row[0])} AND "
            f"{row[1]} = '{row_val.get(row[1])}';"
        )
        conn.commit()
        return
    row = list(row_val.keys())[0]
    row_value = row_val.get(row)
    cursor.execute(
        f"UPDATE {table.lower()} "
        f"SET {column} = {column_value} "
        f"WHERE {row} = {row_value};"
    )
    conn.commit()


def fetchall(table: str, columns: List[str]) -> List[Dict]:
    """Get selected columns from DB"""
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table.lower()}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def fetchone(table: str, target_column: str, column_val: Dict) -> Tuple[str]:
    """Get specific row from DB"""
    column = list(column_val.keys())[0]
    column_val = column_val.get(column)
    cursor.execute(f"SELECT {target_column} FROM {table.lower()} "
                   f"WHERE {column}={column_val};")
    result = cursor.fetchone()
    return result


def delete(table: str, column_val: Dict):
    """Delete data by ID from DB"""
    column = list(column_val.keys())[0]
    val = int(list(column_val.values())[0])
    cursor.execute(f"DELETE FROM {table} WHERE {column}={val}")
    conn.commit()


def clean_table(table: str):
    """Clean all data from table (table itself not remove)"""
    cursor.execute(
        f"TRUNCATE TABLE {table};"
    )
    conn.commit()


def sort(table: str, columns: List[str], filtr: str, order: str = 'DESC') -> List[Dict]:
    """Sort data by column (ASC or DSC)"""
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table.lower()} ORDER BY {filtr} {order}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def create_db_table(table_name: str):
    """Creates table in db"""
    database.create_book_table(table_name)


def get_cursor():
    """Returns cursor"""
    return cursor


def _init_db_():
    """Initialise DB"""
    db_creator = createdb.DbCreator()
    db_creator.__init_db__()


def check_table_empty(table: str) -> bool:
    """Check table is empty or not"""
    cursor.execute(f"SELECT CASE WHEN EXISTS (SELECT * FROM {table} LIMIT 1) THEN 0 ELSE 1 END")
    if cursor.fetchone()[0]:
        return True


def check_table_exist(table: str) -> bool:
    """Check if table exist"""
    cursor.execute("SELECT EXISTS (SELECT * FROM information_schema.tables "
                   f"WHERE table_schema = 'public' AND table_name  = '{table.lower()}');")
    if cursor.fetchone()[0]:
        return True


def check_db_exist():
    table_users_exist = check_table_exist(USERS_TABLE)
    table_progress_exist = check_table_exist(PROGRESS_TABLE)
    table_messages_exist = check_table_exist(MESSAGES_TABLE)
    if table_users_exist and table_progress_exist and table_messages_exist:
        return
    _init_db_()


check_db_exist()
