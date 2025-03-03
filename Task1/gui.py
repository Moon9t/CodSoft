import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import storage
from ttkthemes import ThemedTk

class ModernTodoApp:
    def __init__(self, todo_list):
        # Initalize todo list and GUI stuff
        self.todo_list = todo_list
        self.root = ThemedTk(theme="arc")
        self.root.title("CodSoft Todo List")
        self.root.geometry("800x600")
        self.colors = {
            'bg': '#FFFFFF',
            'text': '#2C3E50',
            'button': '#3498DB',
            'button_hover': '#2980B9',
            'success': '#2ECC71',
            'warning': '#E74C3C'
        }
        self.root.configure(bg=self.colors['bg'])
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        # Setup stles for main frame and butttons
        style = ttk.Style()
        style.configure("Main.TFrame", background=self.colors['bg'])
        style.configure("Action.TButton",
                        padding=10,
                        font=('Helvetica', 11, 'bold'),
                        background=self.colors['button'],
                        foreground=self.colors['text'])
        style.configure("Header.TLabel",
                        font=('Helvetica', 18, 'bold'),
                        background=self.colors['bg'],
                        foreground=self.colors['text'],
                        padding=20)

    def create_widgets(self):
        # Create main frame, listbox, buttons, and statuz bar
        self.main_frame = ttk.Frame(self.root, style="Main.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        header = ttk.Label(self.main_frame, text="Task Management", style="Header.TLabel")
        header.pack(fill=tk.X)
        self.task_frame = ttk.Frame(self.main_frame)
        self.task_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        scrollbar = ttk.Scrollbar(self.task_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox = tk.Listbox(self.task_frame,
                                  selectmode=tk.SINGLE,
                                  bg=self.colors['bg'],
                                  fg=self.colors['text'],
                                  selectbackground=self.colors['button'],
                                  selectforeground='white',
                                  font=('Helvetica', 12),
                                  relief=tk.FLAT,
                                  borderwidth=0,
                                  highlightthickness=1,
                                  highlightcolor=self.colors['button'])
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, pady=20)
        buttons = [
            ("Add Task", self.add_task, "#3498DB"),
            ("Update", self.update_task, "#2980B9"),
            ("Delete", self.delete_task, "#E74C3C"),
            ("Complete", self.complete_task, "#2ECC71")
        ]
        for text, command, color in buttons:
            btn = tk.Button(btn_frame,
                            text=text,
                            command=command,
                            font=('Helvetica', 11, 'bold'),
                            bg=color,
                            fg='white',
                            relief=tk.FLAT,
                            padx=20,
                            pady=10,
                            cursor='hand2')
            btn.pack(side=tk.LEFT, padx=5)
            btn.bind('<Enter>', lambda e, b=btn, c=color: self.on_button_hover(b, c))
            btn.bind('<Leave>', lambda e, b=btn, c=color: self.on_button_leave(b, c))
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.main_frame,
                                    textvariable=self.status_var,
                                    font=('Helvetica', 10),
                                    foreground=self.colors['text'])
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
        self.refresh_listbox()

    def on_button_hover(self, button, base_color):
        # chnage button color on hover
        button.configure(bg=self.adjust_color_brightness(base_color, -20))

    def on_button_leave(self, button, base_color):
        # reset button color when mouse leaves
        button.configure(bg=base_color)

    def adjust_color_brightness(self, color, factor):
        r = int(color[1:3], 16) + factor
        g = int(color[3:5], 16) + factor
        b = int(color[5:7], 16) + factor
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        return f'#{r:02x}{g:02x}{b:02x}'

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for idx, task in enumerate(self.todo_list.tasks, start=1):
            status = "✓" if task.completed else "○"
            self.listbox.insert(tk.END, f" {status}  {task.title}")
            if task.completed:
                self.listbox.itemconfig(idx-1, fg='#95A5A6')
        self.status_var.set(f"Total tasks: {len(self.todo_list.tasks)}")

    def add_task(self):
        dialog = TaskDialog(self.root, "Add New Task")
        if dialog.result:
            title, description = dialog.result
            self.todo_list.add_task(title, description)
            storage.save_tasks(self.todo_list)
            self.refresh_listbox()
            self.show_notification("Task added successfully!")

    def update_task(self):
        selection = self.listbox.curselection()
        if selection:
            task = self.todo_list.tasks[selection[0]]
            dialog = TaskDialog(self.root, "Update Task", task.title, task.description)
            if dialog.result:
                title, description = dialog.result
                self.todo_list.update_task(task.id, title, description)
                storage.save_tasks(self.todo_list)
                self.refresh_listbox()
                self.show_notification("Task updated succesfully!")
        else:
            self.show_notification("Please select a task to update", "warning")

    def delete_task(self):
        selection = self.listbox.curselection()
        if selection:
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
                task = self.todo_list.tasks[selection[0]]
                self.todo_list.delete_task(task.id)
                storage.save_tasks(self.todo_list)
                self.refresh_listbox()
                self.show_notification("Task deleted succesfully!")
        else:
            self.show_notification("Please select a task to delete", "warning")

    def complete_task(self):
        selection = self.listbox.curselection()
        if selection:
            task = self.todo_list.tasks[selection[0]]
            task.mark_complete()
            storage.save_tasks(self.todo_list)
            self.refresh_listbox()
            self.show_notification("Task marked as complete!")
        else:
            self.show_notification("Please select a task to mark as complete", "warning")

    def show_notification(self, message, type="info"):
        self.status_var.set(message)
        self.root.after(3000, lambda: self.status_var.set(f"Total tasks: {len(self.todo_list.tasks)}"))

class TaskDialog:
    def __init__(self, parent, title, initial_title="", initial_description=""):
        self.result = None
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.geometry("400x300")
        dialog.transient(parent)
        dialog.grab_set()
        dialog.configure(bg='#FFFFFF')
        tk.Label(dialog, text="Title:", font=('Helvetica', 12), bg='#FFFFFF', fg='#2C3E50').pack(pady=(20,5))
        self.title_entry = ttk.Entry(dialog, width=40, font=('Helvetica', 11))
        self.title_entry.insert(0, initial_title)
        self.title_entry.pack()
        tk.Label(dialog, text="Description:", font=('Helvetica', 12), bg='#FFFFFF', fg='#2C3E50').pack(pady=(20,5))
        self.desc_entry = tk.Text(dialog, width=40, height=5, font=('Helvetica', 11), wrap=tk.WORD)
        self.desc_entry.insert('1.0', initial_description)
        self.desc_entry.pack()
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)
        for text, command, color in [("Save", self.save, "#3498DB"), ("Cancel", dialog.destroy, "#95A5A6")]:
            btn = tk.Button(btn_frame,
                            text=text,
                            command=command,
                            font=('Helvetica', 11),
                            bg=color,
                            fg='white',
                            relief=tk.FLAT,
                            padx=20,
                            pady=8,
                            cursor='hand2')
            btn.pack(side=tk.LEFT, padx=5)
        dialog.wait_window()

    def save(self):
        title = self.title_entry.get().strip()
        description = self.desc_entry.get('1.0', tk.END).strip()
        if title:
            self.result = (title, description)
            self.title_entry.master.destroy()

def launch_gui(todo_list):
    app = ModernTodoApp(todo_list)
    app.root.mainloop()
