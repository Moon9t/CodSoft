import sqlite3
from todo import Task
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.db_name = "todo.db"
        self.init_database()

    def init_database(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    created_at TEXT,
                    updated_at TEXT,
                    completed BOOLEAN,
                    unique_feature TEXT
                )
            ''')
            conn.commit()

    def save_tasks(self, todo_list):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Clear existing tasks
            cursor.execute('DELETE FROM tasks')
            # Insert all current tasks
            for task in todo_list.tasks:
                cursor.execute('''
                    INSERT INTO tasks (id, title, description, created_at, 
                                     updated_at, completed, unique_feature)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (task.id, task.title, task.description, task.created_at,
                     task.updated_at, task.completed, task.unique_feature))
            conn.commit()

    def load_tasks(self, todo_list):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks')
            rows = cursor.fetchall()
            
            todo_list.tasks = []
            for row in cursor.fetchall():
                task = Task(
                    title=row[1],
                    description=row[2],
                    id=row[0],
                    created_at=row[3],
                    updated_at=row[4],
                    completed=bool(row[5]),
                    unique_feature=row[6]
                )
                todo_list.tasks.append(task)

# Create a global instance
db = DatabaseManager()

def save_tasks(todo_list):
    db.save_tasks(todo_list)

def load_tasks(todo_list):
    db.load_tasks(todo_list)
