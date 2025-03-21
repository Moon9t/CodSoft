import tkinter as tk
from tkinter import ttk, messagebox
from contact_manager import Contact, ContactManager
from ttkthemes import ThemedTk
import re

class ContactBookApp:
    def __init__(self, contact_manager):
        self.root = ThemedTk(theme="arc")
        self.contact_manager = contact_manager
        self.colors = {
            'primary': '#2196F3',
            'secondary': '#FFC107',
            'bg': '#FFFFFF',
            'text': '#212121',
            'light_text': '#757575',
            'error': '#F44336',
            'success': '#4CAF50',
            'warning': '#FF9800',
            'hover': '#1976D2'
        }
        self.setup_ui()
        self.refresh_contacts()

    def setup_ui(self):
        self.root.title("Modern Contact Book")
        self.root.geometry("1000x700")
        self.root.configure(bg=self.colors['bg'])
        
        self.setup_styles()
        self.create_header()
        self.create_main_content()
        self.create_status_bar()

    def setup_styles(self):
        style = ttk.Style()
        style.configure("Header.TLabel", 
                       font=('Helvetica', 24, 'bold'),
                       background=self.colors['bg'],
                       foreground=self.colors['primary'])
        
        style.configure("Search.TEntry",
                       font=('Helvetica', 12),
                       fieldbackground=self.colors['bg'])
        
        style.configure("Contact.Treeview",
                       font=('Helvetica', 11),
                       rowheight=40,
                       background=self.colors['bg'],
                       fieldbackground=self.colors['bg'])
        
        style.configure("Contact.Treeview.Heading",
                       font=('Helvetica', 12, 'bold'),
                       background=self.colors['primary'],
                       foreground='white')

    def create_header(self):
        header_frame = ttk.Frame(self.root, style="Header.TFrame")
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        ttk.Label(header_frame, 
                 text="Contact Book", 
                 style="Header.TLabel").pack(side=tk.LEFT)
        
        search_frame = ttk.Frame(header_frame)
        search_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(50, 0))
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.search_contacts())
        
        search_entry = ttk.Entry(search_frame, 
                               textvariable=self.search_var,
                               font=('Helvetica', 12),
                               style="Search.TEntry")
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        search_entry.insert(0, "Search contacts...")
        search_entry.bind('<FocusIn>', lambda e: self.on_search_focus_in(search_entry))
        search_entry.bind('<FocusOut>', lambda e: self.on_search_focus_out(search_entry))

    def create_main_content(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Buttons frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        buttons = [
            ("Add Contact", self.show_add_dialog, self.colors['primary']),
            ("Delete Selected", self.delete_contact, self.colors['error']),
            ("Export Contacts", self.export_contacts, self.colors['success']),
            ("Import Contacts", self.import_contacts, self.colors['warning'])
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(btn_frame,
                          text=text,
                          command=command,
                          font=('Helvetica', 11),
                          bg=color,
                          fg='white',
                          relief=tk.FLAT,
                          padx=15,
                          pady=8,
                          cursor='hand2')
            btn.pack(side=tk.LEFT, padx=5)
            self.setup_button_hover(btn)
        
        # Treeview
        columns = ("Name", "Phone", "Email", "Address", "Tags")
        self.tree = ttk.Treeview(main_frame, 
                                columns=columns,
                                show="headings",
                                style="Contact.Treeview")
        
        for col in columns:
            self.tree.heading(col, text=col)
            width = 200 if col in ["Name", "Email", "Address"] else 150
            self.tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<Double-1>", self.show_edit_dialog)
        self.tree.bind("<Delete>", lambda e: self.delete_contact())

    def create_status_bar(self):
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(self.root,
                              textvariable=self.status_var,
                              font=('Helvetica', 10),
                              foreground=self.colors['light_text'])
        status_bar.pack(fill=tk.X, padx=20, pady=5)

    def setup_button_hover(self, button):
        original_color = button.cget('bg')
        button.bind('<Enter>', 
                   lambda e: button.configure(bg=self.adjust_color_brightness(original_color, -20)))
        button.bind('<Leave>', 
                   lambda e: button.configure(bg=original_color))

    def adjust_color_brightness(self, color, factor):
        r = int(color[1:3], 16) + factor
        g = int(color[3:5], 16) + factor
        b = int(color[5:7], 16) + factor
        return f'#{max(0, min(255, r)):02x}{max(0, min(255, g)):02x}{max(0, min(255, b)):02x}'

    def show_contact_dialog(self, title, contact=None):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("500x400")
        dialog.configure(bg=self.colors['bg'])
        
        fields = {}
        field_frames = {}
        
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        for i, (field, placeholder) in enumerate([
            ("Name", "Enter full name"),
            ("Phone", "Enter phone number"),
            ("Email", "Enter email address"),
            ("Address", "Enter full address"),
            ("Tags", "Enter tags (comma separated)")
        ]):
            frame = ttk.Frame(main_frame)
            frame.pack(fill=tk.X, pady=10)
            
            ttk.Label(frame,
                     text=field,
                     font=('Helvetica', 11, 'bold')).pack(anchor=tk.W)
            
            entry = ttk.Entry(frame, font=('Helvetica', 11))
            entry.pack(fill=tk.X, pady=(5, 0))
            
            if contact:
                value = getattr(contact, field.lower(), "")
                entry.insert(0, value)
            else:
                entry.insert(0, placeholder)
                entry.bind('<FocusIn>', 
                          lambda e, entry=entry, ph=placeholder: self.on_entry_focus_in(entry, ph))
                entry.bind('<FocusOut>', 
                          lambda e, entry=entry, ph=placeholder: self.on_entry_focus_out(entry, ph))
            
            fields[field.lower()] = entry
            field_frames[field.lower()] = frame
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(20, 0))
        
        for text, command, color in [
            ("Save", lambda: self.save_contact(fields, contact, dialog), self.colors['success']),
            ("Cancel", dialog.destroy, self.colors['warning'])
        ]:
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
            self.setup_button_hover(btn)

    def save_contact(self, fields, existing_contact, dialog):
        values = {k: v.get().strip() for k, v in fields.items()}
        
        # Validation
        if not values["name"] or not values["phone"]:
            messagebox.showerror("Error", "Name and Phone are required!")
            return
        
        if not self.validate_phone(values["phone"]):
            messagebox.showerror("Error", "Invalid phone number format!")
            return
        
        if values["email"] and not self.validate_email(values["email"]):
            messagebox.showerror("Error", "Invalid email format!")
            return
        
        new_contact = Contact(**values)
        if existing_contact:
            new_contact.id = existing_contact.id
            self.contact_manager.update_contact(new_contact)
            self.show_status("Contact updated successfully!", "success")
        else:
            self.contact_manager.add_contact(new_contact)
            self.show_status("New contact added successfully!", "success")
        
        self.refresh_contacts()
        dialog.destroy()

    def validate_phone(self, phone):
        pattern = r'^\+?1?\d{9,15}$'
        return bool(re.match(pattern, phone))

    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def show_status(self, message, status_type="info"):
        color = {
            "success": self.colors['success'],
            "error": self.colors['error'],
            "warning": self.colors['warning'],
            "info": self.colors['primary']
        }.get(status_type, self.colors['text'])
        
        self.status_var.set(message)
        self.root.after(3000, lambda: self.status_var.set(""))

    def export_contacts(self):
        # Add export functionality here
        self.show_status("Export feature coming soon!", "warning")

    def import_contacts(self):
        # Add import functionality here
        self.show_status("Import feature coming soon!", "warning")

    def on_search_focus_in(self, entry):
        if entry.get() == "Search contacts...":
            entry.delete(0, tk.END)

    def on_search_focus_out(self, entry):
        if not entry.get():
            entry.insert(0, "Search contacts...")

    def on_entry_focus_in(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)

    def on_entry_focus_out(self, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)

    def show_add_dialog(self):
        self.show_contact_dialog("Add Contact")

    def show_edit_dialog(self, event):
        item = self.tree.selection()[0]
        contact = self.get_contact_from_item(item)
        self.show_contact_dialog("Edit Contact", contact)

    def delete_contact(self):
        selected = self.tree.selection()
        if not selected:
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this contact?"):
            contact = self.get_contact_from_item(selected[0])
            self.contact_manager.delete_contact(contact.id)
            self.refresh_contacts()

    def get_contact_from_item(self, item):
        values = self.tree.item(item)["values"]
        contacts = self.contact_manager.search_contacts(values[0])
        return next((c for c in contacts if c.phone == values[1]), None)

    def refresh_contacts(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        contacts = self.contact_manager.get_all_contacts()
        for contact in contacts:
            self.tree.insert("", tk.END, values=(contact.name, contact.phone, 
                                               contact.email, contact.address))

    def search_contacts(self):
        term = self.search_var.get()
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        contacts = (self.contact_manager.search_contacts(term) 
                   if term else self.contact_manager.get_all_contacts())
        
        for contact in contacts:
            self.tree.insert("", tk.END, values=(contact.name, contact.phone, 
                                               contact.email, contact.address))