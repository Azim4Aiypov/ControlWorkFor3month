import sqlite3

# Используем check_same_thread=False для поддержки многозадачности
connection = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = connection.cursor()

def init_db():
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
                    (id INTEGER PRIMARY KEY, task_text TEXT, quantity INTEGER, completed INTEGER)''')
    connection.commit()

def get_tasks(filter_type="all"):
    query = "SELECT id, task_text, completed, quantity FROM tasks"
    if filter_type == "completed":
        query += " WHERE completed = 1"
    elif filter_type == "incomplete":
        query += " WHERE completed = 0"
    
    cursor.execute(query)
    return cursor.fetchall()

def add_task_db(task_text, quantity):
    cursor.execute("INSERT INTO tasks (task_text, quantity, completed) VALUES (?, ?, ?)",
                   (task_text, quantity, 0))  # 0 means not completed
    connection.commit()
    return cursor.lastrowid  # Return the ID of the newly added task

def update_task_db(task_id, task_text, quantity, completed=None):
    if completed is not None:
        cursor.execute("UPDATE tasks SET task_text = ?, quantity = ?, completed = ? WHERE id = ?",
                       (task_text, quantity, completed, task_id))
    else:
        cursor.execute("UPDATE tasks SET task_text = ?, quantity = ? WHERE id = ?",
                       (task_text, quantity, task_id))
    connection.commit()

def delete_task_db(task_id):
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    connection.commit()