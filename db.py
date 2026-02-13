import sqlite3


class Database:
    def __init__(self, db_name="habits.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS habit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER,
            day TEXT,
            FOREIGN KEY (habit_id) REFERENCES habits(id)
        )
        """)

        self.conn.commit()

    def add_habit(self, name):
        cursor = self.conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO habits (name) VALUES (?)", (name,))
        self.conn.commit()

    def get_habits(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM habits")
        return [row[0] for row in cursor.fetchall()]

    def add_log(self, habit_name, day):
        cursor = self.conn.cursor()

        cursor.execute("SELECT id FROM habits WHERE name = ?", (habit_name,))
        result = cursor.fetchone()

        if not result:
            return

        habit_id = result[0]

        cursor.execute(
            "INSERT INTO habit_logs (habit_id, day) VALUES (?, ?)",
            (habit_id, day),
        )

        self.conn.commit()

    def get_logs_for_habit(self, habit_name):
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT hl.day
            FROM habit_logs hl
            JOIN habits h ON hl.habit_id = h.id
            WHERE h.name = ?
        """, (habit_name,))

        return [row[0] for row in cursor.fetchall()]
