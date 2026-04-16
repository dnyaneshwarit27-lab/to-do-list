import argparse
import sys
from rich.console import Console
from rich.table import Table
from rich import print as rprint
import database

console = Console()

def main():
    # Initialize database
    database.init_db()
    
    parser = argparse.ArgumentParser(
        description="Advanced To-Do CLI Application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python main.py add \"Buy groceries\" -d \"Milk, eggs, bread\"\n"
               "  python main.py list\n"
               "  python main.py complete 1\n"
               "  python main.py update 1 -s \"In Progress\"\n"
               "  python main.py delete 1"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    parser_add = subparsers.add_parser("add", help="Add a new task")
    parser_add.add_argument("title", type=str, help="Title of the task")
    parser_add.add_argument("-d", "--description", type=str, default="", help="Description of the task")

    # List command
    parser_list = subparsers.add_parser("list", help="List all tasks")
    parser_list.add_argument("-s", "--status", type=str, choices=['Pending', 'Completed', 'In Progress'], help="Filter by status")

    # Update command
    parser_update = subparsers.add_parser("update", help="Update an existing task")
    parser_update.add_argument("id", type=int, help="Task ID")
    parser_update.add_argument("-t", "--title", type=str, help="New title")
    parser_update.add_argument("-d", "--description", type=str, help="New description")
    parser_update.add_argument("-s", "--status", type=str, choices=['Pending', 'Completed', 'In Progress'], help="New status")

    # Complete command
    parser_complete = subparsers.add_parser("complete", help="Mark task as completed")
    parser_complete.add_argument("id", type=int, help="Task ID to mark completed")

    # Delete command
    parser_delete = subparsers.add_parser("delete", help="Delete a task")
    parser_delete.add_argument("id", type=int, help="Task ID to delete")

    args = parser.parse_args()

    if args.command == "add":
        task_id = database.add_task(args.title, args.description)
        rprint(f"[bold green][SUCCESS] Task added successfully with ID: {task_id}[/bold green]")

    elif args.command == "list":
        tasks = database.get_all_tasks()
        if args.status:
            tasks = [t for t in tasks if t[3] == args.status]
            
        if not tasks:
            if args.status:
                rprint(f"[bold yellow]No tasks found with status '{args.status}'.[/bold yellow]")
            else:
                rprint("[bold yellow]No tasks found. Try adding some![/bold yellow]")
        else:
            table = Table(title="To-Do List")
            table.add_column("ID", justify="right", style="cyan", no_wrap=True)
            table.add_column("Title", style="magenta")
            table.add_column("Description", style="white")
            table.add_column("Status", style="bold")
            table.add_column("Created At", style="dim")

            for task in tasks:
                status_color = "green" if task[3] == "Completed" else "yellow" if task[3] == "In Progress" else "red"
                table.add_row(
                    str(task[0]),
                    task[1],
                    task[2],
                    f"[{status_color}]{task[3]}[/{status_color}]",
                    task[4]
                )
            
            console.print(table)

    elif args.command == "update":
        if not any([args.title, args.description, args.status]):
            rprint("[bold red][ERROR] Please provide at least one field to update (-t, -d, -s)[/bold red]")
            sys.exit(1)
        
        success = database.update_task(args.id, args.title, args.description, args.status)
        if success:
            rprint(f"[bold green][SUCCESS] Task {args.id} updated successfully[/bold green]")
        else:
            rprint(f"[bold red][ERROR] Task {args.id} not found[/bold red]")

    elif args.command == "complete":
        success = database.mark_completed(args.id)
        if success:
            rprint(f"[bold green][SUCCESS] Task {args.id} marked as Completed[/bold green]")
        else:
            rprint(f"[bold red][ERROR] Task {args.id} not found[/bold red]")

    elif args.command == "delete":
        success = database.delete_task(args.id)
        if success:
            rprint(f"[bold green][SUCCESS] Task {args.id} deleted successfully[/bold green]")
        else:
            rprint(f"[bold red][ERROR] Task {args.id} not found[/bold red]")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
