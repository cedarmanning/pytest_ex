__all__ = ["Expense", "Food", "Subscription", "Tuition"]
from datetime import datetime, timedelta

# Expense Base Class
class Expense:
    def __init__(self, category, amount):
        self._category = category
        self._amount = amount

    def get_details(self):
        return f"{self._category}: ${self._amount:.2f}"

        # Equality (==)
    def __eq__(self, other):
        if isinstance(other, Expense):
            return self._amount == other._amount
        return NotImplemented

        # Less than (<)
    def __lt__(self, other):
        if isinstance(other, Expense):
            return self._amount < other._amount
        return NotImplemented

        # Greater than (>)
    def __gt__(self, other):
        if isinstance(other, Expense):
            return self._amount > other._amount
        return NotImplemented

# Tuition -> Derived Class
class Tuition(Expense):
    def __init__(self, amount):
        super().__init__("Tuition", amount)
        self._fees = []
        self._scholarships = []

    def apply_scholarship(self, name ,adjustment):
        self._amount -= adjustment
        self._scholarships.append(f"Scholarship: {name}, Amount: ${adjustment:.2f}")

    def add_fee(self, name, adjustment):
        self._amount += adjustment
        self._fees.append(f"Fee: {name}, Amount: ${adjustment:.2f}")
    
    def display(self):
        print(self.get_details())
        print(self._fees)
        print(self._scholarships)

#Subscription -> Derived Class
class Subscription(Expense):
    def __init__(self, date, name, amount):
        super().__init__("Subscription", amount)
        self._date = date
        self._name = name

    def change_plan(self, new_amount):
        self._amount = new_amount

    def cancel(self):
        self._amount = 0
    
    def get_billing_date(self, day_of_month):
        if day_of_month > self._date:
            return (30 - day_of_month) + self._date  # Fix calculation
        return self._date - day_of_month

    def display(self):
        status = "Active" if self._amount > 0 else "Canceled"
        print(f"Subscription: {self._name}")
        print(f"Billing Date: {self._date}")
        print(f"Amount: ${self._amount:.2f}")
        print(f"Status: {status}")

# Food -> Derived Class
class Food(Expense):
    def __init__(self, exp_days, type, amount):
        super().__init__("Food", amount)
        self._purchase_date = datetime.today()
        self._expiration_date = self._purchase_date + timedelta(days=exp_days)
        self._type = type
        self._num_ppl = 0

    def is_expired(self):
        return datetime.today() > self._expiration_date
    
    def split_bill(self, num_ppl):
        if(num_ppl == 0): return
        self._num_ppl = num_ppl
        self._amount /= num_ppl

    def display(self):
        status = "Expired" if self.is_expired() else "Fresh"
        print(f"Food Type: {self._type}")
        print(f"Total Cost: ${self._amount:.2f}")
        print(f"Purchase Date: {self._purchase_date.strftime('%Y-%m-%d')}")

        if self._type in ["Groceries"]:
            print(f"Expiration Date: {self._expiration_date.strftime('%Y-%m-%d')} ({status})")
        if self._type in ["Takeout", "Restaurant"] and self._num_ppl > 0:
            print(f"Split Among: {self._num_ppl} person(s) → Each pays: ${self._amount:.2f}")
