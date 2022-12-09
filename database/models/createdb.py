import psycopg2
from config import db_config
from config.db_config import USERS_TABLE, PROGRESS_TABLE, MESSAGES_TABLE


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
                            telegram_username text,
                            telegram_first_name text,
                            telegram_last_name text,
                            privilege text,
                            registration_timestamp text,
                            current_book text 
                            )""")

    def __create_progress_table(self):
        """Create progress table"""
        with self.conn:
            self.cursor.execute(f"""CREATE TABLE {PROGRESS_TABLE} (
                            id SERIAL PRIMARY KEY,
                            fk_user_id bigint REFERENCES {USERS_TABLE}(telegram_id),
                            last_page int,
                            pages_amount int,
                            book_filename text,
                            read_timestamp text,
                            shedule_read_timestamp text
                            )""")

    def __create_messages_table(self):
        """Create table with bot messages"""
        with self.conn:
            self.cursor.execute(f"""CREATE TABLE {MESSAGES_TABLE} (
                            id int PRIMARY KEY,
                            greeting_msg text,
                            add_book_msg text,
                            book_format_err_msg text,
                            first_book_msg text,
                            same_book_msg text,
                            reeding_complete_msg text
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
        try:
            self.__create_messages_table()
        except Exception as ex:
            print(f'[ERR] PostreSQL: Cant create messages table\n'
                  f'[EX] {ex}')
