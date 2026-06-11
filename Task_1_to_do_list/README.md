# 📝 To-Do List Application

## 📋 Project Overview
A comprehensive To-Do List application developed as a python project. This application helps users manage and organize their tasks efficiently with both Command-Line Interface (CLI) and Graphical User Interface (GUI) versions.

## ✨ Features

### Core Features
- ✅ Create, Read, Update, Delete tasks
- 🎯 Set priority levels (High/Medium/Low)
- 📊 Track task status (Pending/In Progress/Completed)
- 📅 Add due dates and categories
- 🔍 Search and filter tasks
- 📈 View task statistics and completion rates
- 💾 Automatic data persistence using JSON

### Interface Options
- **GUI Version**: User-friendly graphical interface with tkinter
- **CLI Version**: Lightweight command-line interface

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- No external packages required!

### Installation
    ```bash
    # Clone or download the project files
    # Navigate to project directory
    cd todo_app  

    # Run the application (no installation needed!)
        python todo_gui.py     # For GUI version
    # OR
        python todo_cli.py     # For command-line version

        Linux Users Only
        If you get "No module named tkinter" error:

        bash
        sudo apt-get install python3-tk  # Ubuntu/Debian
        sudo dnf install python3-tkinter  # Fedora


### 📁 Project Structure
    # text
        todo_app/
        ├── todo_manager.py   # Core business logic and data management
        ├── todo_cli.py       # Command-line interface
        ├── todo_gui.py       # Graphical user interface
        ├── tasks.json        # Data storage (auto-created on first run)
        ├── requirements.txt  # Dependencies (none required!)
        └── README.md         # This file


### 💻 Usage Guide
    GUI Version
        Add Task: Click "➕ Add Task" button → Fill details → Click "Save"

        View Tasks: Tasks appear in the main table with color coding

        Update Task: Select a task → Modify details in right panel

        Delete Task: Select task → Click "🗑️ Delete Selected"

        Complete Task: Select task → Click "🔄 Complete Selected"

        Filter Tasks: Use dropdown menu to filter by status/priority

        Search Tasks: Type keywords in search box

        View Statistics: Click "📊 Statistics" button

    CLI Version
        text
        Main Menu Options:
        1. ➕ Add New Task
        2. 📋 View All Tasks
        3. ✏️ Update Task
        4. ❌ Delete Task
        5. 🔍 Filter Tasks
        6. 📊 View Statistics
        7. 🏷️ Manage Categories
        8. 💾 Save & Exit

### 🎯 Features in Detail
Task Management
    Title: Required field for task identification

    Description: Optional detailed notes

    Priority: High (🔴), Medium (🟡), Low (🟢)

    Status: Pending (⏳), In Progress (🔄), Completed (✅)

    Due Date: Optional deadline (YYYY-MM-DD format)

    Category: Organize tasks by project/area

    Task Statistics
    Total tasks count

    Completion rate percentage

    Distribution by priority

    Distribution by category

    Status breakdown

## 🔧 Technical Details
    Technologies Used
    Language: Python 3.7+

    GUI Framework: tkinter (built-in)

    Data Storage: JSON (built-in)

    No External Dependencies: 100% Python Standard Library

### Key Concepts Implemented
    Object-Oriented Programming (OOP)

    Data persistence with JSON

    Exception handling

    Type hints for better code quality

    Enumerations for status/priority

    Dataclasses for clean data structures

    MVC-like architecture

### 📊 Sample Output
    #GUI Interface
    text
        [Main Window]
        - Header: To-Do List Manager
        - Task Table: ID | Title | Priority | Status | Due Date | Category
        - Task Details Panel with edit capabilities
        - Statistics Dashboard
    #CLI Interface
    text
        ============================================================
                📝 TO-DO LIST MANAGER - CLI VERSION
        ============================================================

        📋 MAIN MENU:
        1. ➕ Add New Task
        2. 📋 View All Tasks
        3. ✏️ Update Task
        4. ❌ Delete Task
        5. 🔍 Filter Tasks
        6. 📊 View Statistics
        7. 🏷️ Manage Categories
        8. 💾 Save & Exit


### Future Enhancements
    Cloud synchronization

    Task sharing/collaboration

    Email reminders for due dates

    Export tasks to PDF/CSV

    Dark mode theme

    Mobile app version

    Recurring tasks

    Tags and labels

    Task dependencies

    Time tracking

### AUTHOR
  RASIKA KADAM