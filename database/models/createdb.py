import psycopg2
from config import db_config
from config.db_config import USERS_TABLE, BOOKS_TABLE, PROGRESS_TABLE


class DbCreator:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=db_config.DB_HOST,
            dbname=db_config.DB_NAME,
            user=db_config.DB_USER,
            password=db_config.DB_PASSWORD,
            port=db_config.DB_PORT,
        )
        self.cursor = self.conn.cursor()

    def __create_users_table(self):
        """Create users table"""
        with self.conn:
            self.cursor.execute(f"""CREATE TABLE {USERS_TABLE} (
                            telegram_id bigint PRIMARY KEY,
                            privilege text,
                            registration_timestamp text 
                            )""")

    def __create_progress_table(self):
        """Create progress table"""
        with self.conn:
            self.cursor.execute(f"""CREATE TABLE {PROGRESS_TABLE} (
                            id SERIAL PRIMARY KEY,
                            fk_user_id bigint REFERENCES {USERS_TABLE}(telegram_id),
                            last_page text,
                            book_filename text 
                            )""")

    def create_book_table(self, table_name: str):
        """Create books table"""
        with self.conn:
            self.cursor.execute(f"""CREATE TABLE {table_name} (
                            id SERIAL PRIMARY KEY,
                            user_create_id bigint REFERENCES {USERS_TABLE}(telegram_id),
                            part_numb int,
                            part_text text
                            )""")

    def __init_db__(self):
        try:
            self.__create_users_table()
        except Exception as ex:
            print(f'[ERR] PostreSQL: Cant create users table\n'
                  f'[EX] {ex}')
        try:
            self.__create_progress_table()
        except Exception as ex:
            print(f'[ERR] PostreSQL: Cant create progress table\n'
                  f'[EX] {ex}')
