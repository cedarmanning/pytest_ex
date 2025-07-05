from budget import Tuition, Subscription, Food


# Main Functions for input -> using exception handling
def get_float_input(prompt):
    """Gets a float input with error handling."""
    while True:
        try:
            value = float(input(prompt).strip())
            if value < 0:
                print("Value cannot be negative. Try again.")
            else:
                return value
        except ValueError:
            print("Invalid input! Please enter a valid number.")

def get_int_input(prompt, min_value=None, max_value=None):
    """Gets an integer input with optional min/max validation."""
    while True:
        try:
            value = int(input(prompt).strip())
            if min_value is not None and value < min_value:
                print(f"Value must be at least {min_value}. Try again.")
            elif max_value is not None and value > max_value:
                print(f"Value must not exceed {max_value}. Try again.")
            else:
                return value
        except ValueError:
            print("Invalid input! Please enter a valid integer.")

def get_valid_choice(prompt, valid_choices):
    """Ensures input is one of the allowed choices. This for type input or any misc input"""
    while True:
        choice = input(prompt).strip().capitalize()
        if choice in valid_choices:
            return choice
        print(f"Invalid choice! Please enter one of: {', '.join(valid_choices)}.")

def get_string_input(prompt):
    """Enter in valid String"""
    while True:
        try:
            user_input = input(prompt).strip()
            
            if not user_input: 
                raise ValueError("Input cannot be empty. Please try again.")

            return user_input
        
        except ValueError as e:
            print(e)



def main():
    expenses = []  # Store all expenses, will be updated to balanced tree later

    while True:
        """Print Menu for User"""
        print("\n Budget Management System")
        print("1. Add Tuition Expense")
        print("2. Add Subscription Expense")
        print("3. Add Food Expense")
        print("4. View All Expenses")
        print("5. Exit")

        choice = get_int_input("", 1, 5)

        try:
            if choice == 1:  # Tuition Expense
                amount = get_float_input("Enter tuition amount: ")
                tuition = Tuition(amount)
                
                while True:
                    # Tuition Menu
                    print("\n Tuition Options:")
                    print("1. Add Fee")
                    print("2. Apply Scholarship")
                    print("3. View Tuition")
                    print("4. Done")
                    option = get_int_input("", 1, 4)

                    if option == "1":
                        fee_name = get_string_input("Enter fee name: ")
                        fee_amount = get_float_input("Enter fee amount: ")
                        tuition.add_fee(fee_name, fee_amount)

                    elif option == "2":
                        scholarship_name = get_string_input("Enter scholarship name: ")
                        scholarship_amount = get_float_input("Enter scholarship amount: ")
                        tuition.apply_scholarship(scholarship_name, scholarship_amount)

                    elif option == "3":
                        tuition.display()

                    elif option == "4":
                        break

                    else:
                        print(" Invalid choice. Try again.")

                expenses.append(tuition)

            elif choice == 2:  # Subscription Expense
                date = get_int_input("Enter billing date (1-30): ", 1, 30)
                name = get_string_input("Enter subscription name: ")
                amount = get_float_input("Enter monthly cost: ")
                subscription = Subscription(date, name, amount)
                
                while True:
                    # Subscription Menu
                    print("\n Subscription Options:")
                    print("1. Change Plan")
                    print("2. Cancel Subscription")
                    print("3. View Subscription")
                    print("4. Done")
                    option = get_int_input("", 1, 4)

                    if option == 1:
                        new_amount = get_float_input("Enter new plan amount: ")
                        subscription.change_plan(new_amount)

                    elif option == 2:
                        subscription.cancel()

                    elif option == 3:
                        subscription.display()

                    elif option == 4:
                        break
                    else:
                        print(" Invalid choice. Try again.")

                expenses.append(subscription)

            elif choice == 3:  # Food Expense
                exp_days = get_int_input("Enter days until expiration: ", 0)  # No negative days allowed
                food_type = get_valid_choice("Enter food type (Groceries/Takeout/Restaurant): ", ["Groceries", "Takeout", "Restaurant"])
                amount = get_float_input("Enter food expense amount: ")
                food = Food(exp_days, food_type, amount)
                
                if food_type in ["Takeout", "Restaurant"]:
                    split = get_valid_choice("Do you want to split the bill? (Yes/No): ", ["Yes", "No"])
                    if split == "Yes":
                        num_ppl = get_int_input("Enter number of people (at least 1): ", 1)
                        food.split_bill(num_ppl)

                expenses.append(food)

            elif choice == 4:  # View All Expenses
                if not expenses:
                    print("\n No expenses recorded yet.")
                else:
                    print("\n Expense Overview:")
                    for exp in expenses:
                        exp.display()
                        print("-" * 30)

            elif choice == 5:  # Exit
                print(" Quitting program. Goodbye!")
                break

            else:   # error code
                print(" Invalid option. Please choose again.")

        except Exception as e:
            print(f" Unexpected error: {e}. Please try again.")

main()
