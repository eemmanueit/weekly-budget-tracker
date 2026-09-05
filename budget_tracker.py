# ==============================================================================
# PROGRAM: Personal Weekly Budget Tracker and Expense Analyzer
# AUTHOR: Edner Emmanuel
# DATE: September 5, 2026
# DESCRIPTION:
# This program helps users plan, track, and analyze their weekly expenditures.
# It prompts the user for a weekly budget limit and then continuously collects
# expense names and costs. It validates inputs to prevent crashes, calculates
# detailed spending statistics, and appends a summary report to a local log file.
# ==============================================================================

import os
from datetime import datetime

def get_valid_float(prompt_message, allow_zero=False):
    """
    Prompts the user for a numeric input and ensures it is a valid float.
    Uses Exception Handling (try-except) inside a loop to keep prompting the user
    until they provide a valid, positive float number.
    """
    while True:
        # Read input and remove spaces at the beginning and end
        user_input = input(prompt_message).strip()
        try:
            # Try to convert the input string to a decimal float
            value = float(user_input)
            
            # Check if the number is negative
            if value < 0:
                print("Error: Please enter a positive number. Negative values are not allowed.")
            # Check if budget is set to zero when not allowed
            elif value == 0 and not allow_zero:
                print("Error: The budget limit must be greater than zero.")
            else:
                # Input is valid, return the float value
                return value
        except ValueError:
            # Handle case where conversion to float fails (e.g. letters are entered)
            print(f"Error: '{user_input}' is not a valid number. Please enter numeric digits (e.g., 45.50).")

def log_session_to_file(budget_limit, total_spent, remaining, avg_expense, max_expense_name, max_expense_val):
    """
    Appends a summary of the user's weekly budget and spending session to a local text file.
    Includes the date and time of the logging event.
    """
    file_path = "budget_history.txt"
    try:
        # Open file in append ('a') mode, creating it if it doesn't exist.
        # Append ensures that historical data from past runs is never deleted.
        with open(file_path, "a") as file:
            # Get the current system date and time
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
            
            # Write formatted data structures to the file
            file.write("\n" + "="*50 + "\n")
            file.write(f"BUDGET SESSION LOG - {dt_string}\n")
            file.write(f"Weekly Budget Limit: ${budget_limit:.2f}\n")
            file.write(f"Total Money Spent:   ${total_spent:.2f}\n")
            file.write(f"Remaining Balance:   ${remaining:.2f}\n")
            file.write(f"Average Expense:     ${avg_expense:.2f}\n")
            
            # Only log highest expense details if they exist
            if max_expense_name:
                file.write(f"Highest Expense:     {max_expense_name} (${max_expense_val:.2f})\n")
            else:
                file.write("Highest Expense:     None (No expenses recorded)\n")
            file.write("="*50 + "\n")
        print("\n[System Info] Your budget statistics have been successfully appended to budget_history.txt.")
    except IOError as e:
        # Catch any file system input/output errors safely
        print(f"\n[System Error] Could not write to log file: {e}")

def display_summary(budget, expenses, total, remaining, avg, max_name, max_val):
    """
    Prints a clear, user-friendly expense summary table in the terminal.
    """
    print("\n" + "="*50)
    print("           WEEKLY BUDGET ANALYSIS REPORT")
    print("="*50)
    print(f"Weekly Budget Limit:    ${budget:.2f}")
    print(f"Total Expenses Entered:  {len(expenses)}")
    print(f"Total Money Spent:      ${total:.2f}")
    
    # Check if we are over or under budget and format the display
    if remaining >= 0:
        print(f"Remaining Balance:      ${remaining:.2f} (Under Budget)")
        status_message = f"Congratulations! You stayed within your budget by ${remaining:.2f}."
    else:
        abs_deficit = abs(remaining)
        print(f"Remaining Balance:     -${abs_deficit:.2f} (OVER BUDGET!)")
        status_message = f"Warning: You exceeded your weekly budget limit by ${abs_deficit:.2f}!"
        
    print(f"Average Expense Cost:   ${avg:.2f}")
    if max_name:
        print(f"Highest Single Expense: '{max_name}' (${max_val:.2f})")
    else:
        print("Highest Single Expense: None")
    print("-"*50)
    print(status_message)
    print("="*50)

def main():
    """
    Main program control loop that orchestrates the budgeting application.
    """
    print("==================================================")
    print("     Welcome to the Personal Weekly Budget Tracker")
    print("==================================================")
    print("This program helps you budget your money, track expenses,")
    print("and log your spending history to a text file.")
    print("--------------------------------------------------")
    
    # Step 1: Get the user's weekly budget limit with validation
    budget_limit = get_valid_float("Please enter your weekly budget limit (e.g., 150): ")
    
    # Step 2: Initialize lists and trackers for expenses
    expenses = []
    
    print("\nNow, enter your expenses one by one.")
    print("Type 'done' as the name of the expense when you are finished.")
    print("-"*50)
    
    # Step 3: Loop continuously to collect expense names and amounts
    while True:
        expense_name = input("Enter the name of the expense (e.g., Grocery, Rent, Gas): ").strip()
        
        # Check for the exit command (case insensitive)
        if expense_name.lower() == "done":
            break
            
        # Ensure they didn't just press enter
        if not expense_name:
            print("Error: The expense name cannot be blank. Please try again.")
            continue
            
        # Get the corresponding validated cost of the expense
        expense_amount = get_valid_float(f"Enter the cost for '{expense_name}': ", allow_zero=True)
        
        # Store expense details in a dictionary and append to our tracking list
        expenses.append({
            "name": expense_name,
            "amount": expense_amount
        })
        print(f"-> Added: {expense_name} (${expense_amount:.2f})")
        print("-" * 30)

    # Step 4: Check if any expenses were recorded to avoid division-by-zero
    if len(expenses) == 0:
        print("\n" + "="*50)
        print("Summary: No expenses were recorded.")
        print(f"You kept 100% of your weekly budget: ${budget_limit:.2f}")
        print("="*50)
        # Log session with zero values
        log_session_to_file(budget_limit, 0.0, budget_limit, 0.0, "", 0.0)
        return

    # Step 5: Perform statistical calculations
    total_spent = 0.0
    highest_expense_val = -1.0
    highest_expense_name = ""
    
    for item in expenses:
        total_spent += item["amount"]
        if item["amount"] > highest_expense_val:
            highest_expense_val = item["amount"]
            highest_expense_name = item["name"]
            
    remaining_balance = budget_limit - total_spent
    average_expense = total_spent / len(expenses)
    
    # Step 6: Display results on screen
    display_summary(budget_limit, expenses, total_spent, remaining_balance, average_expense, highest_expense_name, highest_expense_val)
    
    # Step 7: Log session to file
    log_session_to_file(budget_limit, total_spent, remaining_balance, average_expense, highest_expense_name, highest_expense_val)

if __name__ == "__main__":
    main()
