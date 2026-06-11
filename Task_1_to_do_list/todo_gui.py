"""
Graphical User Interface To-Do List Application using tkinter
Complete working version with Save functionality
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from todo_manager import TaskManager, Priority, Status

class TodoGUI:
    def __init__(self, root):
        self.root = root
        self.manager = TaskManager()
        self.root.title("📝 To-Do List Manager")
        self.root.geometry("1200x700")
        
        # Configure colors and styles
        self.colors = {
            'bg': '#f0f0f0',
            'header': '#2c3e50',
            'button': '#3498db',
            'button_hover': '#2980b9',
            'delete': '#e74c3c',
            'complete': '#27ae60',
            'pending': '#f39c12',
            'in_progress': '#3498db'
        }
        
        self.setup_styles()
        self.create_widgets()
        self.refresh_task_list()
    
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Header.TLabel', font=('Arial', 16, 'bold'), 
                       foreground='white', background=self.colors['header'])
        style.configure('Task.TFrame', relief='solid', borderwidth=1)
        style.configure('High.TLabel', foreground='red')
        style.configure('Medium.TLabel', foreground='orange')
        style.configure('Low.TLabel', foreground='green')
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors['header'], height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="📝 TO-DO LIST MANAGER", 
                               font=('Arial', 18, 'bold'), 
                               fg='white', bg=self.colors['header'])
        title_label.pack(pady=15)
        
        # Main content area
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Task list
        left_panel = tk.Frame(main_frame, bg=self.colors['bg'])
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Toolbar
        toolbar = tk.Frame(left_panel, bg=self.colors['bg'])
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        tk.Button(toolbar, text="➕ Add Task", command=self.add_task_dialog,
                 bg=self.colors['button'], fg='white', font=('Arial', 10, 'bold'),
                 padx=15, pady=5, cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        tk.Button(toolbar, text="🗑️ Delete Selected", command=self.delete_selected_task,
                 bg=self.colors['delete'], fg='white', font=('Arial', 10, 'bold'),
                 padx=15, pady=5, cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        tk.Button(toolbar, text="📊 Statistics", command=self.show_statistics,
                 bg=self.colors['button'], fg='white', font=('Arial', 10, 'bold'),
                 padx=15, pady=5, cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        tk.Button(toolbar, text="🔄 Complete Selected", command=self.complete_selected_task,
                 bg=self.colors['complete'], fg='white', font=('Arial', 10, 'bold'),
                 padx=15, pady=5, cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        # Search/filter frame
        filter_frame = tk.Frame(left_panel, bg=self.colors['bg'])
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(filter_frame, text="Filter by:", bg=self.colors['bg']).pack(side=tk.LEFT, padx=5)
        
        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var,
                                   values=["All", "Pending", "In Progress", "Completed", 
                                          "High Priority", "Medium Priority", "Low Priority"],
                                   width=20, state='readonly')
        filter_combo.pack(side=tk.LEFT, padx=5)
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_task_list())
        
        tk.Label(filter_frame, text="Search:", bg=self.colors['bg']).pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(filter_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind('<KeyRelease>', lambda e: self.refresh_task_list())
        
        # Task treeview
        tree_frame = tk.Frame(left_panel)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar_y = ttk.Scrollbar(tree_frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.tree = ttk.Treeview(tree_frame, 
                                 columns=('ID', 'Title', 'Priority', 'Status', 'Due Date', 'Category'),
                                 show='headings',
                                 yscrollcommand=scrollbar_y.set,
                                 xscrollcommand=scrollbar_x.set,
                                 height=20)
        
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)
        
        # Define columns
        self.tree.heading('ID', text='ID')
        self.tree.heading('Title', text='Title')
        self.tree.heading('Priority', text='Priority')
        self.tree.heading('Status', text='Status')
        self.tree.heading('Due Date', text='Due Date')
        self.tree.heading('Category', text='Category')
        
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Title', width=300)
        self.tree.column('Priority', width=100, anchor='center')
        self.tree.column('Status', width=120, anchor='center')
        self.tree.column('Due Date', width=120, anchor='center')
        self.tree.column('Category', width=120, anchor='center')
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_task_select)
        
        # Right panel - Task details
        right_panel = tk.Frame(main_frame, bg='white', width=350)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        right_panel.pack_propagate(False)
        
        # Task details frame
        details_frame = tk.LabelFrame(right_panel, text="Task Details", 
                                      font=('Arial', 12, 'bold'),
                                      bg='white', padx=10, pady=10)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        tk.Label(details_frame, text="Title:", font=('Arial', 10, 'bold'),
                bg='white').grid(row=0, column=0, sticky='w', pady=5)
        self.title_label = tk.Label(details_frame, text="", bg='white', 
                                    wraplength=300, justify='left')
        self.title_label.grid(row=0, column=1, sticky='w', pady=5)
        
        # Description
        tk.Label(details_frame, text="Description:", font=('Arial', 10, 'bold'),
                bg='white').grid(row=1, column=0, sticky='nw', pady=5)
        self.desc_text = tk.Text(details_frame, height=5, width=35, wrap=tk.WORD)
        self.desc_text.grid(row=1, column=1, pady=5, padx=(5, 0))
        
        # Priority
        tk.Label(details_frame, text="Priority:", font=('Arial', 10, 'bold'),
                bg='white').grid(row=2, column=0, sticky='w', pady=5)
        self.priority_var = tk.StringVar()
        priority_frame = tk.Frame(details_frame, bg='white')
        priority_frame.grid(row=2, column=1, sticky='w', pady=5)
        
        priorities = [("🔴 High", "High"), ("🟡 Medium", "Medium"), ("🟢 Low", "Low")]
        for text, value in priorities:
            tk.Radiobutton(priority_frame, text=text, variable=self.priority_var,
                          value=value, bg='white', command=self.update_priority).pack(side=tk.LEFT, padx=5)
        
        # Status
        tk.Label(details_frame, text="Status:", font=('Arial', 10, 'bold'),
                bg='white').grid(row=3, column=0, sticky='w', pady=5)
        self.status_var = tk.StringVar()
        status_combo = ttk.Combobox(details_frame, textvariable=self.status_var,
                                   values=["Pending", "In Progress", "Completed"],
                                   state='readonly', width=20)
        status_combo.grid(row=3, column=1, sticky='w', pady=5)
        status_combo.bind('<<ComboboxSelected>>', lambda e: self.update_status())
        
        # Due date
        tk.Label(details_frame, text="Due Date:", font=('Arial', 10, 'bold'),
                bg='white').grid(row=4, column=0, sticky='w', pady=5)
        self.due_date_label = tk.Label(details_frame, text="", bg='white')
        self.due_date_label.grid(row=4, column=1, sticky='w', pady=5)
        
        # Category
        tk.Label(details_frame, text="Category:", font=('Arial', 10, 'bold'),
                bg='white').grid(row=5, column=0, sticky='w', pady=5)
        self.category_label = tk.Label(details_frame, text="", bg='white')
        self.category_label.grid(row=5, column=1, sticky='w', pady=5)
        
        # Created date
        tk.Label(details_frame, text="Created:", font=('Arial', 10, 'bold'),
                bg='white').grid(row=6, column=0, sticky='w', pady=5)
        self.created_label = tk.Label(details_frame, text="", bg='white')
        self.created_label.grid(row=6, column=1, sticky='w', pady=5)
        
        # Update button
        self.update_btn = tk.Button(details_frame, text="✏️ Update Description",
                                   command=self.update_description,
                                   bg=self.colors['button'], fg='white',
                                   font=('Arial', 10, 'bold'), cursor='hand2')
        self.update_btn.grid(row=7, column=0, columnspan=2, pady=15)
        
        self.current_task_id = None
    
    def refresh_task_list(self):
        """Refresh the task list based on filters"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get filtered tasks
        tasks = self.manager.get_all_tasks()
        
        # Apply filters
        filtered_tasks = []
        filter_value = self.filter_var.get()
        search_text = self.search_var.get().lower()
        
        for task in tasks:
            # Apply status/priority filter
            if filter_value != "All":
                if filter_value in ["Pending", "In Progress", "Completed"]:
                    if task.status.value != filter_value:
                        continue
                elif filter_value in ["High Priority", "Medium Priority", "Low Priority"]:
                    if task.priority.value != filter_value.replace(" Priority", ""):
                        continue
            
            # Apply search filter
            if search_text and search_text not in task.title.lower() and \
               search_text not in task.description.lower():
                continue
            
            filtered_tasks.append(task)
        
        # Insert tasks into tree
        for task in filtered_tasks:
            # Set tag for row coloring
            tag = task.status.value.lower().replace(' ', '_')
            
            self.tree.insert('', 'end', values=(
                task.id,
                task.title,
                task.priority.value,
                task.status.value,
                task.due_date if task.due_date else "No due date",
                task.category
            ), tags=(tag,))
        
        # Configure tags
        self.tree.tag_configure('pending', background='#fff3e0')
        self.tree.tag_configure('in_progress', background='#e3f2fd')
        self.tree.tag_configure('completed', background='#e8f5e9')
    
    def on_task_select(self, event):
        """Handle task selection"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        task_id = item['values'][0]
        
        task = self.manager.get_task(task_id)
        if task:
            self.current_task_id = task.id
            self.title_label.config(text=task.title)
            self.desc_text.delete(1.0, tk.END)
            self.desc_text.insert(1.0, task.description)
            self.priority_var.set(task.priority.value)
            self.status_var.set(task.status.value)
            self.due_date_label.config(text=task.due_date if task.due_date else "Not set")
            self.category_label.config(text=task.category)
            self.created_label.config(text=task.created_date)
    
    def add_task_dialog(self):
        """Show dialog to add new task"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Task")
        dialog.geometry("500x500")
        dialog.configure(bg='white')
        
        # Center the dialog
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Main frame with padding
        main_frame = tk.Frame(dialog, bg='white', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        tk.Label(main_frame, text="Add New Task", font=('Arial', 16, 'bold'),
                bg='white', fg=self.colors['header']).pack(pady=(0, 20))
        
        # Title entry
        tk.Label(main_frame, text="Title *", font=('Arial', 10, 'bold'),
                bg='white', anchor='w').pack(fill=tk.X, pady=(0, 5))
        title_entry = tk.Entry(main_frame, width=50, font=('Arial', 10), 
                               relief='solid', borderwidth=1)
        title_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Description
        tk.Label(main_frame, text="Description", font=('Arial', 10, 'bold'),
                bg='white', anchor='w').pack(fill=tk.X, pady=(0, 5))
        desc_text = tk.Text(main_frame, height=5, width=50, 
                           font=('Arial', 10), relief='solid', borderwidth=1)
        desc_text.pack(fill=tk.X, pady=(0, 15))
        
        # Priority
        tk.Label(main_frame, text="Priority", font=('Arial', 10, 'bold'),
                bg='white', anchor='w').pack(fill=tk.X, pady=(0, 5))
        priority_var = tk.StringVar(value="Medium")
        priority_frame = tk.Frame(main_frame, bg='white')
        priority_frame.pack(fill=tk.X, pady=(0, 15))
        
        priorities = [("🔴 High", "High"), ("🟡 Medium", "Medium"), ("🟢 Low", "Low")]
        for text, value in priorities:
            tk.Radiobutton(priority_frame, text=text, variable=priority_var,
                          value=value, bg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=10)
        
        # Due Date
        tk.Label(main_frame, text="Due Date (YYYY-MM-DD)", font=('Arial', 10, 'bold'),
                bg='white', anchor='w').pack(fill=tk.X, pady=(0, 5))
        due_entry = tk.Entry(main_frame, width=30, font=('Arial', 10),
                            relief='solid', borderwidth=1)
        due_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Category
        tk.Label(main_frame, text="Category", font=('Arial', 10, 'bold'),
                bg='white', anchor='w').pack(fill=tk.X, pady=(0, 5))
        category_entry = tk.Entry(main_frame, width=30, font=('Arial', 10),
                                 relief='solid', borderwidth=1)
        category_entry.insert(0, "General")
        category_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        def save_task():
            title = title_entry.get().strip()
            if not title:
                messagebox.showwarning("Warning", "Title cannot be empty!", parent=dialog)
                return
            
            description = desc_text.get(1.0, tk.END).strip()
            priority = Priority(priority_var.get())
            due_date = due_entry.get().strip() if due_entry.get().strip() else None
            category = category_entry.get().strip() if category_entry.get().strip() else "General"
            
            # Save the task
            task = self.manager.add_task(title, description, priority, due_date, category)
            messagebox.showinfo("Success", f"✅ Task '{task.title}' added successfully!", parent=dialog)
            dialog.destroy()
            self.refresh_task_list()
        
        def cancel():
            dialog.destroy()
        
        tk.Button(button_frame, text="💾 Save Task", command=save_task,
                 bg=self.colors['complete'], fg='white', font=('Arial', 11, 'bold'),
                 padx=25, pady=8, cursor='hand2', relief='raised').pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="❌ Cancel", command=cancel,
                 bg='gray', fg='white', font=('Arial', 11, 'bold'),
                 padx=25, pady=8, cursor='hand2', relief='raised').pack(side=tk.LEFT, padx=10)
        
        # Set focus to title entry
        title_entry.focus()
    
    def delete_selected_task(self):
        """Delete the selected task"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task to delete!")
            return
        
        item = self.tree.item(selection[0])
        task_id = item['values'][0]
        task = self.manager.get_task(task_id)
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete task '{task.title}'?"):
            if self.manager.delete_task(task_id):
                messagebox.showinfo("Success", "Task deleted successfully!")
                self.current_task_id = None
                # Clear details panel
                self.title_label.config(text="")
                self.desc_text.delete(1.0, tk.END)
                self.priority_var.set("")
                self.status_var.set("")
                self.due_date_label.config(text="")
                self.category_label.config(text="")
                self.created_label.config(text="")
                self.refresh_task_list()
            else:
                messagebox.showerror("Error", "Failed to delete task!")
    
    def complete_selected_task(self):
        """Mark selected task as completed"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task to complete!")
            return
        
        item = self.tree.item(selection[0])
        task_id = item['values'][0]
        task = self.manager.get_task(task_id)
        
        if task.status.value == "Completed":
            messagebox.showinfo("Info", "Task is already completed!")
            return
        
        if self.manager.update_task(task_id, status="Completed"):
            messagebox.showinfo("Success", f"✅ Task '{task.title}' marked as completed!")
            self.refresh_task_list()
        else:
            messagebox.showerror("Error", "Failed to update task!")
    
    def update_priority(self):
        """Update task priority"""
        if self.current_task_id:
            priority = self.priority_var.get()
            if self.manager.update_task(self.current_task_id, priority=priority):
                self.refresh_task_list()
    
    def update_status(self):
        """Update task status"""
        if self.current_task_id:
            status = self.status_var.get()
            if self.manager.update_task(self.current_task_id, status=status):
                self.refresh_task_list()
    
    def update_description(self):
        """Update task description"""
        if self.current_task_id:
            new_description = self.desc_text.get(1.0, tk.END).strip()
            if self.manager.update_task(self.current_task_id, description=new_description):
                messagebox.showinfo("Success", "Description updated successfully!")
                self.refresh_task_list()
            else:
                messagebox.showerror("Error", "Failed to update description!")
    
    def show_statistics(self):
        """Show task statistics in a new window"""
        stats = self.manager.get_statistics()
        
        stat_window = tk.Toplevel(self.root)
        stat_window.title("Task Statistics")
        stat_window.geometry("450x450")
        stat_window.configure(bg='white')
        
        stat_window.transient(self.root)
        stat_window.grab_set()
        
        # Title
        tk.Label(stat_window, text="📊 Task Statistics", font=('Arial', 16, 'bold'),
                bg='white', fg=self.colors['header']).pack(pady=20)
        
        # Statistics frame
        frame = tk.Frame(stat_window, bg='white')
        frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        stats_text = f"""
        📌 Total Tasks: {stats['total']}
        
        ✅ Completed: {stats['completed']}
        ⏳ Pending: {stats['pending']}
        🔄 In Progress: {stats['in_progress']}
        
        📈 Completion Rate: {stats['completion_rate']:.1f}%
        """
        
        tk.Label(frame, text=stats_text, font=('Arial', 12),
                bg='white', justify=tk.LEFT).pack(anchor='w', pady=10)
        
        # Priority distribution
        high = len(self.manager.get_tasks_by_priority(Priority.HIGH))
        medium = len(self.manager.get_tasks_by_priority(Priority.MEDIUM))
        low = len(self.manager.get_tasks_by_priority(Priority.LOW))
        
        priority_text = f"""
        🎯 Priority Distribution:
        🔴 High: {high}
        🟡 Medium: {medium}
        🟢 Low: {low}
        """
        
        tk.Label(frame, text=priority_text, font=('Arial', 11),
                bg='white', justify=tk.LEFT).pack(anchor='w', pady=10)
        
        # Category distribution
        categories = {}
        for task in self.manager.tasks:
            categories[task.category] = categories.get(task.category, 0) + 1
        
        if categories:
            category_text = "🏷️ Category Distribution:\n"
            for cat, count in sorted(categories.items()):
                category_text += f"   • {cat}: {count}\n"
            
            tk.Label(frame, text=category_text, font=('Arial', 11),
                    bg='white', justify=tk.LEFT).pack(anchor='w', pady=10)
        
        tk.Button(stat_window, text="Close", command=stat_window.destroy,
                 bg=self.colors['button'], fg='white', font=('Arial', 10, 'bold'),
                 padx=20, pady=8, cursor='hand2').pack(pady=20)
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoGUI(root)
    app.run()