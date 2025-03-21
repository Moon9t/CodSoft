import sqlite3
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Contact:
    name: str
    phone: str
    email: str
    address: str
    id: Optional[int] = None

class ContactManager:
    def __init__(self):
        self.conn = sqlite3.connect('contacts.db')
        self.create_table()

    def create_table(self):
        query = '''CREATE TABLE IF NOT EXISTS contacts
                  (id INTEGER PRIMARY KEY,
                   name TEXT NOT NULL,
                   phone TEXT NOT NULL,
                   email TEXT,
                   address TEXT)'''
        self.conn.execute(query)
        self.conn.commit()

    def add_contact(self, contact: Contact) -> int:
        query = '''INSERT INTO contacts (name, phone, email, address)
                  VALUES (?, ?, ?, ?)'''
        cursor = self.conn.execute(query, (contact.name, contact.phone, 
                                         contact.email, contact.address))
        self.conn.commit()
        return cursor.lastrowid

    def get_all_contacts(self) -> List[Contact]:
        query = 'SELECT id, name, phone, email, address FROM contacts'
        cursor = self.conn.execute(query)
        return [Contact(name, phone, email, address, id) 
                for id, name, phone, email, address in cursor.fetchall()]

    def search_contacts(self, term: str) -> List[Contact]:
        query = '''SELECT id, name, phone, email, address FROM contacts
                  WHERE name LIKE ? OR phone LIKE ?'''
        cursor = self.conn.execute(query, (f'%{term}%', f'%{term}%'))
        return [Contact(name, phone, email, address, id) 
                for id, name, phone, email, address in cursor.fetchall()]

    def update_contact(self, contact: Contact):
        query = '''UPDATE contacts 
                  SET name=?, phone=?, email=?, address=?
                  WHERE id=?'''
        self.conn.execute(query, (contact.name, contact.phone, contact.email,
                                contact.address, contact.id))
        self.conn.commit()

    def delete_contact(self, contact_id: int):
        query = 'DELETE FROM contacts WHERE id=?'
        self.conn.execute(query, (contact_id,))
        self.conn.commit()