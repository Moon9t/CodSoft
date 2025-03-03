import argparse
import sys
from storage import save_tasks, load_tasks
from todo import TodoList
import storage
from gui import launch_gui
from voice import launch_voice_interface
from ai import prioritize_tasks

def parse_arguments():
    # parse args for mode selectin
    parser = argparse.ArgumentParser(description="CodSoft Innovative To-Do List Application")
    parser.add_argument('--mode', choices=['cli', 'gui', 'voice'], default='cli', help="Select interface mode")
    return parser.parse_args()

def cli_mode(todo_list):
    print("Welcome to CodSoft To-Do List (CLI Mode)")
    while True:
        print("\nCurrent Tasks:")
        if not todo_list.tasks:
            print(" No tasks available.")
        for idx, task in enumerate(todo_list.tasks, start=1):
            status = "✓" if task.completed else " "
            print(f" {idx}. [{status}] {task.title} - {task.description}")
        print("\nOptions: [a]dd, [u]pdate, [d]elete, [c]omplete, [p]rioritize (AI), [q]uit")
        choice = input("Select an option: ").strip().lower()
        if choice == 'a':
            title = input("Title: ")
            description = input("Description: ")
            todo_list.add_task(title, description)
            storage.save_tasks(todo_list)
        elif choice == 'u':
            try:
                task_num = int(input("Task number to update: "))
                task = todo_list.tasks[task_num - 1]
                new_title = input(f"New title (leave empty to keep '{task.title}'): ")
                new_description = input(f"New description (leave empty to keep '{task.description}'): ")
                todo_list.update_task(task.id, title=new_title or None, description=new_description or None)
                storage.save_tasks(todo_list)
            except (IndexError, ValueError):
                print("Invalid task number.")
        elif choice == 'd':
            try:
                task_num = int(input("Task number to delete: "))
                task = todo_list.tasks[task_num - 1]
                todo_list.delete_task(task.id)
                storage.save_tasks(todo_list)
            except (IndexError, ValueError):
                print("Invalid task number.")
        elif choice == 'c':
            try:
                task_num = int(input("Task number to mark complete: "))
                task = todo_list.tasks[task_num - 1]
                task.mark_complete()
                storage.save_tasks(todo_list)
            except (IndexError, ValueError):
                print("Invalid task number.")
        elif choice == 'p':
            print("Running AI prioiritization...")
            prioritize_tasks(todo_list)
            storage.save_tasks(todo_list)
        elif choice == 'q':
            print("Exiting...")
            sys.exit(0)
        else:
            print("Option not implemented yet.")

def main():
    args = parse_arguments()  # initalize args
    todo_list = TodoList()
    storage.load_tasks(todo_list)  # load saved tasks

    if args.mode == 'gui':
        launch_gui(todo_list)
    elif args.mode == 'voice':
        launch_voice_interface(todo_list)
    else:
        cli_mode(todo_list)

if __name__ == "__main__":
    main()
