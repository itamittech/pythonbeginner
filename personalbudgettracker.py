# Personal Budget Tracker
print("Welcome to your friendly Personal Budget Tracker !!")

# Step 1: Ask user for daily income
income = float(input("Enter your total income for today: ₹"))

# Step 2: Ask user for daily expenses
expenses = float(input("Enter your total expenses for today: ₹"))

# Step 3: Ask user for rent expense
rent_expense = float(input("What is your expense for rent today: ₹"))

# Optional note
optional_note = input("Anything that you would like to tell as an optional note: ")

# Saving goal
daily_saving_goal = float(input("Enter your daily saving goal: ₹"))

# Step 4: Calculate net savings
net_savings = income - expenses - rent_expense

# Step 5: Print results
print("\n----- Daily Budget Summary -----")

print(f"Total Income: ₹{income:.2f}")
print(f"Total Expenses: ₹{expenses:.2f}")
print(f"Rent Expense: ₹{rent_expense:.2f}")
print(f"Net Savings: ₹{net_savings:.2f}")

print(f"\nToday you earned ₹{income:.2f} and spent ₹{expenses:.2f} "
      f"plus rent of ₹{rent_expense:.2f}.")
print(f"Your note: {optional_note}")

print(f"\nYour daily saving goal was: ₹{daily_saving_goal:.2f}")

# Intelligent Goal Analysis
if net_savings > daily_saving_goal:
    print(f"🎉 Excellent! You exceeded your goal by ₹{net_savings - daily_saving_goal:.2f}")

elif net_savings == daily_saving_goal:
    print("✅ Perfect! You achieved your saving goal exactly!")

else:
    print(f"⚠️ You missed your goal by ₹{daily_saving_goal - net_savings:.2f}")
