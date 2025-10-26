# gui_app.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import os
import sys

# Add 'expense_db' to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'expense_db'))
from tracker import ExpenseTracker


class ExpenseTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🪙 Expense Tracker Pro")
        self.root.geometry("900x650")
        
        # 🔒 LOCK WINDOW SIZE — no maximize, no resize
        self.root.resizable(False, False)
        self.root.maxsize(900, 650)
        self.root.minsize(900, 650)

        # Load background image
        self.bg_image = None
        bg_path = os.path.join("src", "city.jpg")
        if os.path.exists(bg_path):
            try:
                from PIL import Image, ImageTk
                img = Image.open(bg_path)
                img = img.resize((900, 650), Image.Resampling.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(img)
            except ImportError:
                print("⚠️ PIL not installed. Install with: pip install Pillow")
                self.bg_image = None
        else:
            print("⚠️ src/city.jpg not found. Using solid background.")

        # Create main canvas
        self.canvas = tk.Canvas(root, width=900, height=650, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Draw background image
        if self.bg_image:
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        else:
            self.canvas.create_rectangle(0, 0, 900, 650, fill="#f0f8ff", outline="")

        # Cyan color scheme
        self.colors = {
            'bg': '#f0f8ff',
            'card': '#ffffff',
            'accent': '#4fc3f7',
            'gold': '#00bcd4',
            'green': '#4caf50',
            'red': '#ff6b6b',
            'text': '#000000',
            'subtext': '#555555',
            'border': '#cccccc',
        }

        self.tracker = ExpenseTracker()
        self.setup_ui()
        self.refresh_data()

    def setup_ui(self):
        # Header bar (blue)
        self.canvas.create_rectangle(
            20, 20, 880, 100,
            fill=self.colors['accent'],
            outline="",
            tags="header"
        )
        self.canvas.create_text(
            450, 60,
            text="🪙 Expense Tracker Pro",
            font=("Segoe UI", 24, "bold"),
            fill="white",
            tags="header_text"
        )

        # Left panel - Add Expense (with inner padding to simulate rounded corners)
        self.canvas.create_rectangle(
            20, 120, 370, 630,
            fill=self.colors['card'],
            outline=self.colors['border'],
            width=2,
            tags="left_panel"
        )
        # Inner area (simulates rounded corners via padding)
        self.canvas.create_rectangle(
            30, 130, 360, 620,
            fill=self.colors['card'],
            outline="",
            tags="left_inner"
        )
        self.canvas.create_text(
            195, 140,
            text="➕ Add New Expense",
            font=("Segoe UI", 16, "bold"),
            fill=self.colors['gold'],
            tags="add_title"
        )

        # Category
        self.canvas.create_text(40, 160, text="Category:", font=("Segoe UI", 11), fill=self.colors['text'], anchor="w")
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(
            self.canvas,
            textvariable=self.category_var,
            values=["Food", "Transport", "Bills", "Shopping", "Entertainment", "Health", "Other"],
            font=("Segoe UI", 11),
            state="readonly"
        )
        self.canvas.create_window(195, 180, window=self.category_combo, width=300, anchor="n")
        self.category_combo.current(0)

        # Amount
        self.canvas.create_text(40, 220, text="Amount (₱):", font=("Segoe UI", 11), fill=self.colors['text'], anchor="w")
        self.amount_entry = tk.Entry(
            self.canvas,
            font=("Segoe UI", 11),
            bg="#fafafa",
            fg="#000000",
            insertbackground="#000000",
            relief=tk.SUNKEN,
            bd=1
        )
        self.canvas.create_window(195, 240, window=self.amount_entry, width=300, anchor="n")

        # Date
        self.canvas.create_text(40, 280, text="Date:", font=("Segoe UI", 11), fill=self.colors['text'], anchor="w")
        self.date_entry = DateEntry(
            self.canvas,
            width=18,
            background='#fafafa',
            foreground='#000000',
            borderwidth=2,
            date_pattern='yyyy-mm-dd',
            font=("Segoe UI", 11),
            selectbackground=self.colors['gold'],
            selectforeground='black',
            normalbackground='#fafafa',
            normalforeground='#000000',
            weekendbackground='#e0f7fa',
            weekendforeground='#000000',
            headersbackground=self.colors['accent'],
            headersforeground='white'
        )
        self.canvas.create_window(195, 300, window=self.date_entry, width=300, anchor="n")
        self.date_entry.set_date(datetime.now())

        # Description
        self.canvas.create_text(40, 340, text="Description:", font=("Segoe UI", 11), fill=self.colors['text'], anchor="w")
        self.desc_entry = tk.Entry(
            self.canvas,
            font=("Segoe UI", 11),
            bg="#fafafa",
            fg="#000000",
            insertbackground="#000000",
            relief=tk.SUNKEN,
            bd=1
        )
        self.canvas.create_window(195, 360, window=self.desc_entry, width=300, anchor="n")

        # Add Button
        self.add_btn = tk.Button(
            self.canvas,
            text="💵 ADD EXPENSE",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['green'],
            fg="white",
            activebackground="#43a047",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.add_expense,
            padx=15,
            pady=8,
            borderwidth=0,
            highlightthickness=0
        )
        self.canvas.create_window(195, 420, window=self.add_btn, width=300, anchor="n")
        self.add_btn.bind("<Enter>", lambda e: self.add_btn.config(bg="#43a047"))
        self.add_btn.bind("<Leave>", lambda e: self.add_btn.config(bg=self.colors['green']))

        # Right panel - Weekly Summary
        self.canvas.create_rectangle(
            390, 120, 880, 300,
            fill=self.colors['card'],
            outline=self.colors['border'],
            width=2,
            tags="summary_panel"
        )
        # Inner padding
        self.canvas.create_rectangle(
            400, 130, 870, 290,
            fill=self.colors['card'],
            outline="",
            tags="summary_inner"
        )
        self.canvas.create_text(
            635, 160,
            text="📊 Weekly Summary",
            font=("Segoe UI", 14, "bold"),
            fill=self.colors['gold'],
            tags="summary_title"
        )
        self.summary_text = self.canvas.create_text(
            635, 210,
            text="No expenses this week",
            font=("Segoe UI", 11),
            fill=self.colors['subtext'],
            justify="center",
            width=450,
            tags="summary_content"
        )

        # Recent Expenses Header
        self.canvas.create_rectangle(
            390, 310, 880, 350,
            fill=self.colors['card'],
            outline=self.colors['border'],
            width=2,
            tags="list_header"
        )
        self.canvas.create_text(
            400, 330,
            text="📝 Recent Expenses",
            font=("Segoe UI", 14, "bold"),
            fill=self.colors['gold'],
            anchor="w",
            tags="list_title"
        )

        # Delete Button
        self.delete_btn = tk.Button(
            self.canvas,
            text="🗑️ Delete Selected",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors['red'],
            fg="white",
            activebackground="#ff5252",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.delete_expense
        )
        self.canvas.create_window(860, 330, window=self.delete_btn, anchor="e")
        self.delete_btn.bind("<Enter>", lambda e: self.delete_btn.config(bg="#ff5252"))
        self.delete_btn.bind("<Leave>", lambda e: self.delete_btn.config(bg=self.colors['red']))

        # Treeview for expenses (positioned correctly now)
        tree_frame = tk.Frame(self.canvas, bg=self.colors['card'], bd=0)
        self.canvas.create_window(635, 360, window=tree_frame, width=480, height=200, anchor="n", tags="tree_frame")

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Date", "Category", "Amount", "Description"),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=8
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Description", text="Description")

        self.tree.column("ID", width=50)
        self.tree.column("Date", width=100)
        self.tree.column("Category", width=100)
        self.tree.column("Amount", width=100)
        self.tree.column("Description", width=200)

        self.tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)

        # Style Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
            background=self.colors['bg'],
            foreground=self.colors['text'],
            fieldbackground=self.colors['bg'],
            font=("Segoe UI", 10),
            rowheight=25,
            borderwidth=0
        )
        style.configure("Treeview.Heading",
            background=self.colors['accent'],
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            borderwidth=0
        )
        style.map('Treeview',
            background=[('selected', self.colors['gold'])],
            foreground=[('selected', 'black')]
        )

    def add_expense(self):
        category = self.category_var.get()
        amount_str = self.amount_entry.get().strip()
        date = self.date_entry.get()
        description = self.desc_entry.get().strip()

        if not amount_str:
            messagebox.showerror("Error", "Please enter an amount!")
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be positive!")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid amount!")
            return

        self.tracker.add_expense(category, amount, date, description)

        self.amount_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.date_entry.set_date(datetime.now())

        self.refresh_data()
        messagebox.showinfo("Success", f"Added ₱{amount:.2f} to {category}!")

    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an expense to delete!")
            return

        item = self.tree.item(selected[0])
        expense_id = item['values'][0]

        confirm = messagebox.askyesno("Confirm", f"Delete expense #{expense_id}?")
        if confirm:
            self.tracker.delete_expense(expense_id)
            self.refresh_data()
            messagebox.showinfo("Success", "Expense deleted!")

    def refresh_data(self):
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        expenses = self.tracker.get_all_expenses()
        for expense in expenses:
            exp_id, category, amount, date, description = expense
            self.tree.insert("", tk.END, values=(exp_id, date, category, f"₱{amount:.2f}", description))

        # Refresh summary
        summary_dict = self.tracker.get_summary_by_category(7)
        if summary_dict:
            total = sum(summary_dict.values())
            sorted_summary = sorted(summary_dict.items(), key=lambda x: x[1], reverse=True)
            summary_lines = []
            for category, amount in sorted_summary[:5]:
                summary_lines.append(f"{category}: ₱{amount:,.2f}")
            summary_text = "\n".join(summary_lines) + f"\n\nTOTAL: ₱{total:,.2f}"
            self.canvas.itemconfig(self.summary_text, text=summary_text, fill=self.colors['text'])
        else:
            self.canvas.itemconfig(self.summary_text, text="No expenses this week", fill=self.colors['subtext'])


def main():
    root = tk.Tk()
    app = ExpenseTrackerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()