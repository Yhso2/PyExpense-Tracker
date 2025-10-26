import sqlite3
import os
from datetime import datetime, timedelta
from collections import defaultdict

class ExpenseTracker:
    def __init__(self, db_name="expenses.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Initialize the SQLite database and create tables if they don't exist."""
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
        """Add a new expense to the database."""
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
        """Retrieve all expenses from the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
        expenses = cursor.fetchall()
        conn.close()
        return expenses
    
    def get_expenses_by_period(self, days=7):
        """Get expenses for the last N days."""
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
        """Get spending summary grouped by category."""
        expenses = self.get_expenses_by_period(days)
        summary = defaultdict(float)
        
        for expense in expenses:
            category = expense[1]
            amount = expense[2]
            summary[category] += amount
        
        return dict(summary)
    
    def delete_expense(self, expense_id):
        """Delete an expense by ID."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
        conn.close()


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Print a nice header for the application."""
    print("\n" + "="*50)
    print("💰  EXPENSE TRACKER  💰".center(50))
    print("="*50 + "\n")


def print_menu():
    """Display the main menu."""
    print("┌─────────────────────────────────────────┐")
    print("│  1. Add Expense                         │")
    print("│  2. View All Expenses                   │")
    print("│  3. View Weekly Summary                 │")
    print("│  4. View Monthly Summary                │")
    print("│  5. Delete Expense                      │")
    print("│  6. Exit                                │")
    print("└─────────────────────────────────────────┘")


def add_expense_interface(tracker):
    """Interface for adding a new expense."""
    print("\n📝 ADD NEW EXPENSE")
    print("-" * 40)
    
    category = input("Category (e.g., Food, Transport, Bills): ").strip()
    if not category:
        print("❌ Category cannot be empty!")
        return
    
    try:
        amount = float(input("Amount (₱): "))
        if amount <= 0:
            print("❌ Amount must be positive!")
            return
    except ValueError:
        print("❌ Invalid amount!")
        return
    
    date_input = input("Date (YYYY-MM-DD) [press Enter for today]: ").strip()
    date = date_input if date_input else None
    
    description = input("Description (optional): ").strip()
    
    tracker.add_expense(category, amount, date, description)
    print(f"\n✅ Expense added: ₱{amount:.2f} for {category}")


def view_all_expenses(tracker):
    """Display all expenses."""
    expenses = tracker.get_all_expenses()
    
    if not expenses:
        print("\n📭 No expenses recorded yet!")
        return
    
    print("\n📊 ALL EXPENSES")
    print("-" * 80)
    print(f"{'ID':<5} {'Date':<12} {'Category':<15} {'Amount':<12} {'Description':<30}")
    print("-" * 80)
    
    for expense in expenses:
        exp_id, category, amount, date, description = expense
        print(f"{exp_id:<5} {date:<12} {category:<15} ₱{amount:<11.2f} {description:<30}")
    
    total = sum(exp[2] for exp in expenses)
    print("-" * 80)
    print(f"{'TOTAL:':<44} ₱{total:.2f}")


def view_summary(tracker, days, period_name):
    """Display spending summary for a period."""
    summary = tracker.get_summary_by_category(days)
    
    if not summary:
        print(f"\n📭 No expenses in the last {period_name}!")
        return
    
    print(f"\n📈 {period_name.upper()} SUMMARY")
    print("-" * 50)
    
    total = sum(summary.values())
    
    # Sort by amount (highest first)
    sorted_summary = sorted(summary.items(), key=lambda x: x[1], reverse=True)
    
    for category, amount in sorted_summary:
        percentage = (amount / total) * 100
        bar_length = int(percentage / 2)
        bar = "█" * bar_length
        print(f"{category:<15} ₱{amount:>8.2f}  {bar} {percentage:.1f}%")
    
    print("-" * 50)
    print(f"{'TOTAL SPENT:':<15} ₱{total:>8.2f}")
    print(f"\n💡 You spent ₱{total:.2f} in the last {period_name}!")


def delete_expense_interface(tracker):
    """Interface for deleting an expense."""
    view_all_expenses(tracker)
    
    try:
        exp_id = int(input("\nEnter expense ID to delete (0 to cancel): "))
        if exp_id == 0:
            return
        
        confirm = input(f"Are you sure you want to delete expense #{exp_id}? (y/n): ").lower()
        if confirm == 'y':
            tracker.delete_expense(exp_id)
            print(f"✅ Expense #{exp_id} deleted!")
    except ValueError:
        print("❌ Invalid ID!")

def main():
    tracker = ExpenseTracker()
    
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            add_expense_interface(tracker)
        elif choice == '2':
            view_all_expenses(tracker)
        elif choice == '3':
            view_summary(tracker, 7, "week")
        elif choice == '4':
            view_summary(tracker, 30, "month")
        elif choice == '5':
            delete_expense_interface(tracker)
        elif choice == '6':
            print("\n👋 Thanks for using Expense Tracker! Goodbye!\n")
            break
        else:
            print("❌ Invalid choice! Please try again.")
        
        input("\nPress Enter to continue...")