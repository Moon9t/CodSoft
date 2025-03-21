from contact_manager import ContactManager
from gui import ContactBookApp

def main():
    contact_manager = ContactManager()
    app = ContactBookApp(contact_manager)
    app.root.mainloop()

if __name__ == "__main__":
    main()