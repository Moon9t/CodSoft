import uuid
from datetime import datetime

class Task:
    def __init__(self, title, description="", unique_feature=None, id=None, created_at=None, updated_at=None, completed=False):
        self.id = id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()
        self.completed = completed
        self.unique_feature = unique_feature  # For AI suggestions or metadata

    def mark_complete(self):
        self.completed = True
        self.updated_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "completed": self.completed,
            "unique_feature": self.unique_feature,
        }

    @staticmethod
    def from_dict(data):
        return Task(
            title=data.get("title", ""),
            description=data.get("description", ""),
            unique_feature=data.get("unique_feature"),
            id=data.get("id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            completed=data.get("completed", False),
        )

class TodoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, description="", unique_feature=None):
        task = Task(title, description, unique_feature)
        self.tasks.append(task)

    def update_task(self, task_id, title=None, description=None):
        for task in self.tasks:
            if task.id == task_id:
                if title:
                    task.title = title
                if description:
                    task.description = description
                task.updated_at =  datetime.now().isoformat()
                break

    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task.id != task_id]
