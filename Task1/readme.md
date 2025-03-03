# CodSoft Advanced Todo List Application

A feature-rich todo list application with multiple interfaces and SQLite storage. This application demonstrates modern Python development practices with a focus on modularity and extensibility.

## Features

- **Multiple Interface Modes:**
  - Command Line Interface (CLI)
  - Graphical User Interface (GUI)
  - Simulated Voice Interface

- **Task Management:**
  - Create, Read, Update, Delete (CRUD) operations
  - Mark tasks as complete
  - Task prioritization
  - Persistent storage using SQLite

- **AI-Enhanced Features:**
  - Task prioritization suggestions
  - Unique feature tracking per task

## Project Structure

```
CodSoft/ 
    Task1/      
        ├── main.py          # Application entry point 
        ├── todo.py          # Core task and todolist classes 
        ├── storage.py       # SQLite database management 
        ├── ai.py            # AI prioritization features 
        ├── gui.py           # Tkinter GUI implementation 
        ├── voice.py         # Voice interface simulation 
        └── todo.db          # SQLite database file
```

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Moon9t/CodSoft.git
    cd CodSoft/Task1
    ```

2. **Ensure Python 3.x is installed on your system**

3. **Install required dependencies:**
    ```bash
    pip install tkinter
    ```

## Usage

Launch the application in your preferred mode:

### CLI Mode
```bash
python main.py --mode cli
```

### GUI Mode
```bash
python main.py --mode gui
```

### Voice Mode
```bash
python main.py --mode voice
```

## Interface Commands

### CLI Mode
- `a`: Add new task
- `u`: Update existing task
- `d`: Delete task
- `c`: Complete task
- `p`: AI prioritize tasks
- `q`: Quit application

### GUI Mode
- Click "Add" to create new task
- Select task and click "Update" to modify
- Select task and click "Delete" to remove
- Select task and click "Complete" to mark as done

### Voice Mode (Simulated)
- `add`: Create new task
- `update`: Modify existing task
- `delete`: Remove task
- `complete`: Mark task as done
- `list`: Show all tasks
- `quit`: Exit voice mode

## Technical Details

- **Storage:** SQLite database for persistent storage
- **GUI:** Tkinter for graphical interface
- **Task Properties:**
  - Unique ID
  - Title
  - Description
  - Creation timestamp
  - Last updated timestamp
  - Completion status
  - AI-suggested features

## Future Enhancements

- Real voice recognition integration
- Cloud synchronization
- Advanced AI task analysis
- Mobile application interface
- Task categories and tags
- Due dates and reminders
- Multi-user support
- Task sharing capabilities

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

<!-- BuiltByMoon9t -->


