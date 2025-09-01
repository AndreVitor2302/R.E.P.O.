import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

# Banco de dados
def init_db():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('SELECT id, description FROM tasks')
    tasks = c.fetchall()
    conn.close()
    return tasks

def add_task_db(description):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('INSERT INTO tasks (description) VALUES (?)', (description,))
    conn.commit()
    conn.close()

def remove_task_db(task_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

# Interface Tkinter
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ToDo List")
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        self.listbox = tk.Listbox(self.frame, width=40)
        self.listbox.pack()

        self.add_button = tk.Button(self.frame, text="Add Task", command=self.add_task)
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.remove_button = tk.Button(self.frame, text="Remove Task", command=self.remove_task)
        self.remove_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.refresh_button = tk.Button(self.frame, text="Refresh", command=self.refresh_tasks)
        self.refresh_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.refresh_tasks()

    def refresh_tasks(self):
        self.listbox.delete(0, tk.END)
        self.tasks = get_tasks()
        for task in self.tasks:
            self.listbox.insert(tk.END, f"{task[1]}")

    def add_task(self):
        task = simpledialog.askstring("Add Task", "Enter the task:")
        if task:
            add_task_db(task)
            self.refresh_tasks()

    def remove_task(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Select a task to remove.")
            return
        task_id = self.tasks[selected[0]][0]
        remove_task_db(task_id)
        self.refresh_tasks()

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
