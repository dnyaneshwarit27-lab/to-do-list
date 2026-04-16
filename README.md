# Advanced To-Do CLI Application

A complete Python command-line interface (CLI) to-do application with a clean, modular structure and SQLite database integration.

## Features
- **Database Integration**: Data is stored persistently in a local `todos.db` SQLite database.
- **Full CRUD Operations**: Create, Read, Update, Delete tasks.
- **Rich CLI Interface**: Utilizes the `rich` library to render a beautiful CLI table and colored output.
- **Modular Design**: Separated concerns connecting database logic (`database.py`) and command-line execution (`main.py`).

## Requirements
- Python 3.x
- `rich` (for beautiful CLI text formatting)

## Installation
1. Clone or navigate to the project directory:
   ```bash
   cd "to do list"
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
The application is run via `main.py`.

### Add a Task
Add a task with a title and an optional description.
```bash
python main.py add "Buy groceries" -d "Milk, eggs, and bread"
```

### List Tasks
View all tasks in a beautifully formatted table.
```bash
python main.py list
```
Filter tasks by status ("Pending", "Completed", "In Progress"):
```bash
python main.py list -s "Pending"
```

### Update a Task
Update multiple fields at once (title, description, or status) using the Task ID.
```bash
python main.py update 1 -s "In Progress"
python main.py update 1 -t "Buy groceries and drinks" -d "Milk, eggs, bread, and soda"
```

### Complete a Task
Directly mark a task as 'Completed'.
```bash
python main.py complete 1
```

### Delete a Task
Delete a task by its ID.
```bash
python main.py delete 1
```

## Available Commands Summary
Run `python main.py -h` or `python main.py --help` to see all available commands and options.
