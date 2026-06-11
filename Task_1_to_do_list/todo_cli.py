"""
Command-Line To-Do List Application
"""

import sys
from todo_manager import TaskManager, Priority, Status

class TodoCLI:
    def __init__(self):
        self.manager = TaskManager()
    
    def clear_screen(self):
        """Clear terminal screen"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print application header"""
        print("=" * 60)
        print("           📝 TO-DO LIST MANAGER - CLI VERSION")
        print("=" * 60)
    
    def print_menu(self):
        """Print main menu"""
        print("\n📋 MAIN MENU:")
        print("  1. ➕ Add New Task")
        print("  2. 📋 View All Tasks")
        print("  3. ✏️ Update Task")
        print("  4. ❌ Delete Task")
        print("  5. 🔍 Filter Tasks")
        print("  6. 📊 View Statistics")
        print("  7. 🏷️ Manage Categories")
        print("  8. 💾 Save & Exit")
        print("-" * 60)
    
    def print_task(self, task, index=None):
        """Print a single task"""
        priority_colors = {
            Priority.HIGH: "🔴 HIGH",
            Priority.MEDIUM: "🟡 MEDIUM",
            Priority.LOW: "🟢 LOW"
        }
        
        status_icons = {
            Status.PENDING: "⏳",
            Status.IN_PROGRESS: "🔄",
            Status.COMPLETED: "✅"
        }
        
        prefix = f"{index}. " if index else ""
        print(f"\n{prefix}[ID: {task.id}] {task.title}")
        print(f"   📝 Description: {task.description if task.description else 'No description'}")
        print(f"   🎯 Priority: {priority_colors[task.priority]}")
        print(f"   📊 Status: {status_icons[task.status]} {task.status.value}")
        print(f"   📅 Created: {task.created_date}")
        print(f"   ⏰ Due Date: {task.due_date if task.due_date else 'Not set'}")
        print(f"   🏷️ Category: {task.category}")
        print("-" * 40)
    
    def add_task_flow(self):
        """Flow for adding a new task"""
        print("\n✨ ADD NEW TASK")
        title = input("Enter task title: ").strip()
        if not title:
            print("❌ Title cannot be empty!")
            return
        
        description = input("Enter description (optional): ").strip()
        
        print("\nPriority levels:")
        print("  1. 🔴 High")
        print("  2. 🟡 Medium")
        print("  3. 🟢 Low")
        priority_choice = input("Select priority (1-3) [Default: 2]: ").strip()
        
        priority_map = {"1": Priority.HIGH, "2": Priority.MEDIUM, "3": Priority.LOW}
        priority = priority_map.get(priority_choice, Priority.MEDIUM)
        
        due_date = input("Enter due date (YYYY-MM-DD) [optional]: ").strip()
        if not due_date:
            due_date = None
        
        category = input("Enter category [Default: General]: ").strip()
        if not category:
            category = "General"
        
        task = self.manager.add_task(title, description, priority, due_date, category)
        print(f"\n✅ Task '{task.title}' added successfully with ID: {task.id}")
    
    def view_tasks_flow(self):
        """Flow for viewing tasks"""
        print("\n📋 VIEW TASKS")
        print("Sort by:")
        print("  1. Priority (Default)")
        print("  2. Date Created")
        print("  3. Due Date")
        
        choice = input("Select sorting option (1-3) [Default: 1]: ").strip()
        sort_map = {"1": "priority", "2": "date", "3": "due_date"}
        sort_by = sort_map.get(choice, "priority")
        
        tasks = self.manager.get_all_tasks(sort_by)
        
        if not tasks:
            print("\n📭 No tasks found! Add some tasks first.")
            return
        
        print(f"\n{'=' * 60}")
        print(f"Total Tasks: {len(tasks)}")
        print(f"{'=' * 60}")
        
        for i, task in enumerate(tasks, 1):
            self.print_task(task, i)
    
    def update_task_flow(self):
        """Flow for updating a task"""
        print("\n✏️ UPDATE TASK")
        task_id = input("Enter task ID to update: ").strip()
        
        try:
            task_id = int(task_id)
        except ValueError:
            print("❌ Invalid task ID!")
            return
        
        task = self.manager.get_task(task_id)
        if not task:
            print(f"❌ Task with ID {task_id} not found!")
            return
        
        print("\nCurrent task details:")
        self.print_task(task)
        
        print("\nWhat would you like to update?")
        print("  1. Title")
        print("  2. Description")
        print("  3. Priority")
        print("  4. Status")
        print("  5. Due Date")
        print("  6. Category")
        print("  7. Multiple fields")
        
        choice = input("Select option (1-7): ").strip()
        
        updates = {}
        
        if choice == "1":
            updates['title'] = input("New title: ").strip()
        elif choice == "2":
            updates['description'] = input("New description: ").strip()
        elif choice == "3":
            print("\nPriority levels:")
            print("  1. 🔴 High")
            print("  2. 🟡 Medium")
            print("  3. 🟢 Low")
            p_choice = input("Select priority (1-3): ").strip()
            priority_map = {"1": "High", "2": "Medium", "3": "Low"}
            if p_choice in priority_map:
                updates['priority'] = priority_map[p_choice]
        elif choice == "4":
            print("\nStatus options:")
            print("  1. ⏳ Pending")
            print("  2. 🔄 In Progress")
            print("  3. ✅ Completed")
            s_choice = input("Select status (1-3): ").strip()
            status_map = {"1": "Pending", "2": "In Progress", "3": "Completed"}
            if s_choice in status_map:
                updates['status'] = status_map[s_choice]
        elif choice == "5":
            updates['due_date'] = input("New due date (YYYY-MM-DD): ").strip()
        elif choice == "6":
            updates['category'] = input("New category: ").strip()
        elif choice == "7":
            print("\nEnter new values (press Enter to keep current):")
            title = input(f"Title [{task.title}]: ").strip()
            if title:
                updates['title'] = title
            
            desc = input(f"Description [{task.description}]: ").strip()
            if desc:
                updates['description'] = desc
            
            print(f"Priority [{task.priority.value}]: ")
            print("  Options: High, Medium, Low")
            priority = input().strip()
            if priority in ['High', 'Medium', 'Low']:
                updates['priority'] = priority
            
            print(f"Status [{task.status.value}]: ")
            print("  Options: Pending, In Progress, Completed")
            status = input().strip()
            if status in ['Pending', 'In Progress', 'Completed']:
                updates['status'] = status
            
            due = input(f"Due Date [{task.due_date}]: ").strip()
            if due:
                updates['due_date'] = due
            
            cat = input(f"Category [{task.category}]: ").strip()
            if cat:
                updates['category'] = cat
        
        if updates:
            if self.manager.update_task(task_id, **updates):
                print("\n✅ Task updated successfully!")
            else:
                print("\n❌ Failed to update task!")
        else:
            print("\nℹ️ No updates made.")
    
    def delete_task_flow(self):
        """Flow for deleting a task"""
        print("\n❌ DELETE TASK")
        task_id = input("Enter task ID to delete: ").strip()
        
        try:
            task_id = int(task_id)
        except ValueError:
            print("❌ Invalid task ID!")
            return
        
        task = self.manager.get_task(task_id)
        if not task:
            print(f"❌ Task with ID {task_id} not found!")
            return
        
        print("\nTask to delete:")
        self.print_task(task)
        
        confirm = input("\nAre you sure you want to delete this task? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            if self.manager.delete_task(task_id):
                print("\n✅ Task deleted successfully!")
            else:
                print("\n❌ Failed to delete task!")
        else:
            print("\nℹ️ Deletion cancelled.")
    
    def filter_tasks_flow(self):
        """Flow for filtering tasks"""
        print("\n🔍 FILTER TASKS")
        print("Filter by:")
        print("  1. Status")
        print("  2. Priority")
        print("  3. Category")
        
        choice = input("Select filter type (1-3): ").strip()
        
        filtered_tasks = []
        
        if choice == "1":
            print("\nStatus:")
            print("  1. Pending")
            print("  2. In Progress")
            print("  3. Completed")
            s_choice = input("Select status: ").strip()
            status_map = {"1": Status.PENDING, "2": Status.IN_PROGRESS, "3": Status.COMPLETED}
            if s_choice in status_map:
                filtered_tasks = self.manager.get_tasks_by_status(status_map[s_choice])
        elif choice == "2":
            print("\nPriority:")
            print("  1. High")
            print("  2. Medium")
            print("  3. Low")
            p_choice = input("Select priority: ").strip()
            priority_map = {"1": Priority.HIGH, "2": Priority.MEDIUM, "3": Priority.LOW}
            if p_choice in priority_map:
                filtered_tasks = self.manager.get_tasks_by_priority(priority_map[p_choice])
        elif choice == "3":
            category = input("Enter category name: ").strip()
            filtered_tasks = self.manager.get_tasks_by_category(category)
        
        if not filtered_tasks:
            print("\n📭 No tasks match the filter criteria.")
        else:
            print(f"\n📋 Found {len(filtered_tasks)} task(s):")
            for i, task in enumerate(filtered_tasks, 1):
                self.print_task(task, i)
    
    def statistics_flow(self):
        """Display task statistics"""
        print("\n📊 TASK STATISTICS")
        print("=" * 40)
        
        stats = self.manager.get_statistics()
        
        print(f"📌 Total Tasks: {stats['total']}")
        print(f"✅ Completed: {stats['completed']}")
        print(f"⏳ Pending: {stats['pending']}")
        print(f"🔄 In Progress: {stats['in_progress']}")
        print(f"📈 Completion Rate: {stats['completion_rate']:.1f}%")
        
        # Priority distribution
        high = len(self.manager.get_tasks_by_priority(Priority.HIGH))
        medium = len(self.manager.get_tasks_by_priority(Priority.MEDIUM))
        low = len(self.manager.get_tasks_by_priority(Priority.LOW))
        
        print("\n🎯 Priority Distribution:")
        print(f"  🔴 High: {high}")
        print(f"  🟡 Medium: {medium}")
        print(f"  🟢 Low: {low}")
        
        # Category distribution
        categories = {}
        for task in self.manager.tasks:
            categories[task.category] = categories.get(task.category, 0) + 1
        
        if categories:
            print("\n🏷️ Category Distribution:")
            for cat, count in sorted(categories.items()):
                print(f"  {cat}: {count}")
    
    def categories_flow(self):
        """Manage categories"""
        print("\n🏷️ MANAGE CATEGORIES")
        
        # Get unique categories
        categories = set()
        for task in self.manager.tasks:
            categories.add(task.category)
        
        if categories:
            print("\nExisting categories:")
            for i, cat in enumerate(sorted(categories), 1):
                task_count = len(self.manager.get_tasks_by_category(cat))
                print(f"  {i}. {cat} ({task_count} tasks)")
        else:
            print("\nNo categories found.")
    
    def run(self):
        """Main application loop"""
        while True:
            self.clear_screen()
            self.print_header()
            self.print_menu()
            
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == "1":
                self.add_task_flow()
                input("\nPress Enter to continue...")
            elif choice == "2":
                self.view_tasks_flow()
                input("\nPress Enter to continue...")
            elif choice == "3":
                self.update_task_flow()
                input("\nPress Enter to continue...")
            elif choice == "4":
                self.delete_task_flow()
                input("\nPress Enter to continue...")
            elif choice == "5":
                self.filter_tasks_flow()
                input("\nPress Enter to continue...")
            elif choice == "6":
                self.statistics_flow()
                input("\nPress Enter to continue...")
            elif choice == "7":
                self.categories_flow()
                input("\nPress Enter to continue...")
            elif choice == "8":
                print("\n💾 Saving and exiting... Goodbye! 👋")
                sys.exit(0)
            else:
                print("\n❌ Invalid choice! Please try again.")
                input("\nPress Enter to continue...")

if __name__ == "__main__":
    app = TodoCLI()
    app.run()