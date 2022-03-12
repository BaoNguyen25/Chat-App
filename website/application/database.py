import sqlite3
from sqlite3 import Error
from datetime import datetime
import time

FILE = "messages.db"
PLAYLIST_TABLE = "messages"


class DataBase:
    """
    connect with sqlite3 database
    """
    def __init__(self):
        """
        connect to database file and create cursor
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect(FILE)
        except Error as e:
            print(e)

        self.cursor = self.conn.cursor()
        self._create_table()

    def close(self):
        """
        close the database connection
        :return: None
        """
        self.conn.close()

    def _create_table(self):
        """
        create a new one database table
        :return: None
        """
        query = f"""CREATE TABLE IF NOT EXISTS {PLAYLIST_TABLE}
                    (name TEXT, content TEXT, time Date, id INTEGER PRIMARY KEY AUTOINCREMENT)"""
        self.cursor.execute(query)
        self.conn.commit()

    def get_all_messages(self, limit=100, name=None):
        """
        return all messages
        :param limit: int
        :param name: None
        :return: list[dict]
        """
        if not name:
            query = f"SELECT * FROM {PLAYLIST_TABLE}"
            self.cursor.execute(query)
        else:
            query = f"SELECT * FROM {PLAYLIST_TABLE} WHERE NAME = ?"
            self.cursor.execute(query, (name,))

        result = self.cursor.fetchall()

        # sorted by date

        results = []
        for r in sorted(result, key=lambda x: x[3], reverse=True)[:limit]:
            name, content, date, _id = r
            data = {"name": name, "message": content, "time": str(date)}
            results.append(data)

        return list(reversed(results))

    def get_message_by_name(self, name, limit=100):
        """
        get messages by user name
        :param name: str
        :param limit: int
        :return: list
        """
        return self.get_all_messages(limit, name)

    def save_message(self, name, msg):
        """
        save message in the table
        :param name: str
        :param msg: str
        :return: None
        """
        query = f"INSERT INTO {PLAYLIST_TABLE} VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (name, msg, datetime.now(), None))
        self.conn.commit()