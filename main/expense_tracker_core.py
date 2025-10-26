# main/expense_tracker_core.py
import sqlite3
from datetime import datetime, timedelta
from collections import defaultdict


class ExpenseTracker:
    def __init__(self, db_name="expenses.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                description TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    def add_expense(self, category, amount, date=None, description=""):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (category, amount, date, description)
            VALUES (?, ?, ?, ?)
        ''', (category, amount, date, description))
        conn.commit()
        conn.close()
        return True
    
    def get_all_expenses(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
        expenses = cursor.fetchall()
        conn.close()
        return expenses
    
    def get_expenses_by_period(self, days=7):
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM expenses 
            WHERE date >= ? 
            ORDER BY date DESC
        ''', (start_date,))
        expenses = cursor.fetchall()
        conn.close()
        return expenses
    
    def get_summary_by_category(self, days=7):
        expenses = self.get_expenses_by_period(days)
        summary = defaultdict(float)
        for expense in expenses:
            category = expense[1]
            amount = expense[2]
            summary[category] += amount
        return dict(summary)
    
    def delete_expense(self, expense_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
        conn.close()