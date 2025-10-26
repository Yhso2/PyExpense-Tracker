import matplotlib.pyplot as plt
from expense_tracker import ExpenseTracker
from datetime import datetime, timedelta
from collections import defaultdict

def visualize_by_category(days=30):
    """Create a pie chart of expenses by category."""
    tracker = ExpenseTracker()
    summary = tracker.get_summary_by_category(days)
    
    if not summary:
        print(f"No expenses in the last {days} days!")
        return
    
    categories = list(summary.keys())
    amounts = list(summary.values())
    
    # Create figure with better styling
    plt.figure(figsize=(10, 6))
    colors = plt.cm.Set3(range(len(categories)))
    
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', 
            startangle=90, colors=colors, textprops={'fontsize': 10})
    plt.title(f'Expenses by Category (Last {days} Days)', 
              fontsize=14, fontweight='bold', pad=20)
    plt.axis('equal')
    
    # Add total spent
    total = sum(amounts)
    plt.text(0, -1.3, f'Total Spent: ₱{total:.2f}', 
             ha='center', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.show()


def visualize_daily_spending(days=30):
    """Create a bar chart of daily spending."""
    tracker = ExpenseTracker()
    expenses = tracker.get_expenses_by_period(days)
    
    if not expenses:
        print(f"No expenses in the last {days} days!")
        return
    
    # Group expenses by date
    daily_spending = defaultdict(float)
    for expense in expenses:
        date = expense[3]
        amount = expense[2]
        daily_spending[date] += amount
    
    # Sort by date
    dates = sorted(daily_spending.keys())
    amounts = [daily_spending[date] for date in dates]
    
    # Create figure
    plt.figure(figsize=(12, 6))
    plt.bar(dates, amounts, color='#06b6d4', alpha=0.8, edgecolor='#0891b2', linewidth=1.5)
    
    plt.title(f'Daily Spending (Last {days} Days)', 
              fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Amount (₱)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add average line
    avg_spending = sum(amounts) / len(amounts)
    plt.axhline(y=avg_spending, color='red', linestyle='--', 
                linewidth=2, label=f'Average: ₱{avg_spending:.2f}')
    plt.legend()
    
    plt.tight_layout()
    plt.show()


def visualize_category_comparison(days=30):
    """Create a horizontal bar chart comparing categories."""
    tracker = ExpenseTracker()
    summary = tracker.get_summary_by_category(days)
    
    if not summary:
        print(f"No expenses in the last {days} days!")
        return
    
    # Sort by amount
    sorted_items = sorted(summary.items(), key=lambda x: x[1], reverse=True)
    categories = [item[0] for item in sorted_items]
    amounts = [item[1] for item in sorted_items]
    
    # Create figure
    plt.figure(figsize=(10, 8))
    colors = plt.cm.viridis(range(len(categories)))
    
    bars = plt.barh(categories, amounts, color=colors, edgecolor='black', linewidth=1.2)
    
    # Add value labels on bars
    for i, (bar, amount) in enumerate(zip(bars, amounts)):
        plt.text(amount + max(amounts)*0.01, i, f'₱{amount:.2f}', 
                va='center', fontsize=10, fontweight='bold')
    
    plt.title(f'Spending by Category (Last {days} Days)', 
              fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Amount (₱)', fontsize=12)
    plt.ylabel('Category', fontsize=12)
    plt.grid(axis='x', alpha=0.3, linestyle='--')
    
    total = sum(amounts)
    plt.text(0.5, -0.15, f'Total: ₱{total:.2f}', 
             transform=plt.gca().transAxes, ha='center', 
             fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.show()


def main():
    """Visualization menu."""
    print("\n" + "="*50)
    print("📊  EXPENSE VISUALIZER  📊".center(50))
    print("="*50 + "\n")
    
    print("1. Pie Chart - Expenses by Category")
    print("2. Bar Chart - Daily Spending")
    print("3. Horizontal Bar - Category Comparison")
    print("4. Exit")
    
    choice = input("\nChoose visualization (1-4): ").strip()
    
    if choice == '1':
        days = input("Number of days to analyze (default 30): ").strip()
        days = int(days) if days else 30
        visualize_by_category(days)
    elif choice == '2':
        days = input("Number of days to analyze (default 30): ").strip()
        days = int(days) if days else 30
        visualize_daily_spending(days)
    elif choice == '3':
        days = input("Number of days to analyze (default 30): ").strip()
        days = int(days) if days else 30
        visualize_category_comparison(days)
    elif choice == '4':
        print("Goodbye!")
        return
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()