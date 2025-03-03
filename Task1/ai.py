import random

def prioritize_tasks(todo_list):
    # A simple demonstration: assign a random priority to each task's unique_feature field
    priorities = ['Low', 'Medium', 'High', 'Critical']
    for task in todo_list.tasks:
        # Only update if not already set
        if not task.unique_feature:
            task.unique_feature = f"Priority: {random.choice(priorities)}"
            print(f"Task '{task.title}' assigned {task.unique_feature}.")
        else:
            print(f"Task '{task.title}' already has feature: {task.unique_feature}.")
