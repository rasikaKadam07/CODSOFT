"""
Task Manager Module - Handles all task operations
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class Priority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class Status(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

@dataclass
class Task:
    """Task data structure"""
    id: int
    title: str
    description: str
    priority: Priority
    status: Status
    created_date: str
    due_date: Optional[str]
    category: str
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority.value,
            'status': self.status.value,
            'created_date': self.created_date,
            'due_date': self.due_date,
            'category': self.category
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            priority=Priority(data['priority']),
            status=Status(data['status']),
            created_date=data['created_date'],
            due_date=data['due_date'],
            category=data['category']
        )

class TaskManager:
    """Manages all task operations"""
    
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks: List[Task] = []
        self.next_id = 1
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(task) for task in data]
                    if self.tasks:
                        self.next_id = max(task.id for task in self.tasks) + 1
            except (json.JSONDecodeError, FileNotFoundError):
                self.tasks = []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        with open(self.filename, 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=2)
    
    def add_task(self, title: str, description: str = "", priority: Priority = Priority.MEDIUM,
                 due_date: str = None, category: str = "General") -> Task:
        """Add a new task"""
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            priority=priority,
            status=Status.PENDING,
            created_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            due_date=due_date,
            category=category
        )
        self.tasks.append(task)
        self.next_id += 1
        self.save_tasks()
        return task
    
    def update_task(self, task_id: int, **kwargs) -> bool:
        """Update task attributes"""
        task = self.get_task(task_id)
        if not task:
            return False
        
        for key, value in kwargs.items():
            if hasattr(task, key):
                if key == 'priority' and value:
                    task.priority = Priority(value)
                elif key == 'status' and value:
                    task.status = Status(value)
                else:
                    setattr(task, key, value)
        
        self.save_tasks()
        return True
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID"""
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            return True
        return False
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get task by ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_tasks_by_status(self, status: Status) -> List[Task]:
        """Get tasks filtered by status"""
        return [task for task in self.tasks if task.status == status]
    
    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        """Get tasks filtered by priority"""
        return [task for task in self.tasks if task.priority == priority]
    
    def get_tasks_by_category(self, category: str) -> List[Task]:
        """Get tasks filtered by category"""
        return [task for task in self.tasks if task.category.lower() == category.lower()]
    
    def get_all_tasks(self, sort_by: str = "priority") -> List[Task]:
        """Get all tasks with sorting"""
        if sort_by == "priority":
            priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
            return sorted(self.tasks, key=lambda t: priority_order[t.priority])
        elif sort_by == "date":
            return sorted(self.tasks, key=lambda t: t.created_date, reverse=True)
        elif sort_by == "due_date":
            return sorted(self.tasks, key=lambda t: t.due_date if t.due_date else "9999-12-31")
        return self.tasks
    
    def get_statistics(self) -> Dict:
        """Get task statistics"""
        total = len(self.tasks)
        completed = len(self.get_tasks_by_status(Status.COMPLETED))
        pending = len(self.get_tasks_by_status(Status.PENDING))
        in_progress = len(self.get_tasks_by_status(Status.IN_PROGRESS))
        
        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'in_progress': in_progress,
            'completion_rate': (completed / total * 100) if total > 0 else 0
        }