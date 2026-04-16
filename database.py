import sqlite3
from typing import List, Tuple, Optional
from datetime import datetime
import os

# Define database file in the same directory as the script
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "todos.db")

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL DEFAULT 'Pending',
                created_at TEXT NOT NULL
            )
        ''')
        conn.commit()

def add_task(title: str, description: str = "") -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO tasks (title, description, status, created_at) VALUES (?, ?, 'Pending', ?)",
                       (title, description, created_at))
        conn.commit()
        return int(cursor.lastrowid or 0)

def get_all_tasks() -> List[Tuple]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, description, status, created_at FROM tasks")
        return cursor.fetchall()

def get_task_by_id(task_id: int) -> Optional[Tuple]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, description, status, created_at FROM tasks WHERE id = ?", (task_id,))
        return cursor.fetchone()

def update_task(task_id: int, title: Optional[str] = None, description: Optional[str] = None, status: Optional[str] = None) -> bool:
    task = get_task_by_id(task_id)
    if not task:
        return False
    
    new_title = title if title is not None else task[1]
    new_desc = description if description is not None else task[2]
    new_status = status if status is not None else task[3]

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET title = ?, description = ?, status = ? WHERE id = ?",
                       (new_title, new_desc, new_status, task_id))
        conn.commit()
        return True

def delete_task(task_id: int) -> bool:
    task = get_task_by_id(task_id)
    if not task:
        return False

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        return True

def mark_completed(task_id: int) -> bool:
    return update_task(task_id, status='Completed')
