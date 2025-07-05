import pytest
from budget import Expense, Tuition, Subscription, Food
from datetime import datetime, timedelta

### **Test Expense (Base Class)**
@pytest.fixture
def sample_expense():
    return Expense("Miscellaneous", 100)

def test_expense_initialization(sample_expense):
    assert sample_expense._category == "Miscellaneous"
    assert sample_expense._amount == 100

def test_expense_get_details(sample_expense):
    assert sample_expense.get_details() == "Miscellaneous: $100.00"


### **Test Tuition Class**
@pytest.fixture
def sample_tuition():
    return Tuition(5000)

def test_tuition_initialization(sample_tuition):
    assert sample_tuition._category == "Tuition"
    assert sample_tuition._amount == 5000
    assert sample_tuition._fees == []
    assert sample_tuition._scholarships == []

def test_apply_scholarship(sample_tuition):
    sample_tuition.apply_scholarship("Merit", 1000)
    assert sample_tuition._amount == 4000
    assert "Scholarship: Merit, Amount: $1000.00" in sample_tuition._scholarships

def test_add_fee(sample_tuition):
    sample_tuition.add_fee("Lab Fee", 300)
    assert sample_tuition._amount == 5300
    assert "Fee: Lab Fee, Amount: $300.00" in sample_tuition._fees

def test_tuition_display(sample_tuition, capsys):
    sample_tuition.apply_scholarship("Need-Based", 1500)
    sample_tuition.add_fee("Library Fee", 200)
    sample_tuition.display()
    captured = capsys.readouterr()
    assert "Tuition: $3700.00" in captured.out
    assert "Fee: Library Fee, Amount: $200.00" in captured.out
    assert "Scholarship: Need-Based, Amount: $1500.00" in captured.out


### **Test Subscription Class**
@pytest.fixture
def sample_subscription():
    return Subscription(15, "Netflix", 15.99)
    
def test_subscription_initialization(sample_subscription):
    assert sample_subscription._category == "Subscription"
    assert sample_subscription._amount == 15.99
    assert sample_subscription._name == "Netflix"
    assert sample_subscription._date == 15

def test_change_plan(sample_subscription):
    sample_subscription.change_plan(19.99)
    assert sample_subscription._amount == 19.99

def test_cancel_subscription(sample_subscription):
    sample_subscription.cancel()
    assert sample_subscription._amount == 0

def test_get_billing_date(sample_subscription):
    assert sample_subscription.get_billing_date(10) == 5
    assert sample_subscription.get_billing_date(20) == 25
    assert sample_subscription.get_billing_date(15) == 0

def test_subscription_display(sample_subscription, capsys):
    sample_subscription.display()
    captured = capsys.readouterr()
    assert "Subscription: Netflix" in captured.out
    assert "Billing Date: 15" in captured.out
    assert "Amount: $15.99" in captured.out
    assert "Status: Active" in captured.out

    sample_subscription.cancel()
    sample_subscription.display()
    captured = capsys.readouterr()
    assert "Status: Canceled" in captured.out


### **Test Food Class**
@pytest.fixture
def sample_food():
    return Food(5, "Takeout", 30)

def test_food_initialization(sample_food):
    assert sample_food._category == "Food"
    assert sample_food._amount == 30
    assert sample_food._type == "Takeout"
    assert sample_food._num_ppl == 0
    assert isinstance(sample_food._purchase_date, datetime)
    assert isinstance(sample_food._expiration_date, datetime)

def test_food_is_expired():
    food = Food(-1, "Groceries", 50)  # Expiration already passed
    assert food.is_expired() is True

    food = Food(5, "Groceries", 50)  # Fresh for 5 more days
    assert food.is_expired() is False

def test_food_split_bill(sample_food):
    sample_food.split_bill(3)
    assert sample_food._num_ppl == 3
    assert sample_food._amount == 10  # Each person pays $10

def test_food_split_bill_invalid(sample_food):
    sample_food.split_bill(0)
    assert sample_food._num_ppl == 0  # Should not update

def test_food_display(sample_food, capsys):
    sample_food.split_bill(2)
    sample_food.display()
    captured = capsys.readouterr()
    assert "Food Type: Takeout" in captured.out
    assert "Total Cost: $15.00" in captured.out  # 30 split among 2
    assert "Split Among: 2 person(s)" in captured.out

def test_food_display_no_split(capsys):  #  capsys must be an argument
    food = Food(3, "Takeout", 20)
    food.display()
    
    captured = capsys.readouterr() 
    assert "Split Among" not in captured.out 

### **Test Expense (Base Class) OP OVERLOADS!**
@pytest.fixture
def sample_expenses():
    return Expense("Miscellaneous", 100), Expense("Groceries", 200), Expense("Tuition", 5000)

def test_expense_equality(sample_expenses):
    exp1, exp2, _ = sample_expenses
    duplicate_exp1 = Expense("Other", 100)
    
    assert exp1 == duplicate_exp1  
    assert exp1 != exp2            

def test_expense_comparison(sample_expenses):
    exp1, exp2, exp3 = sample_expenses
    
    assert exp1 < exp2
    assert exp2 < exp3
    assert exp3 > exp1
    assert not (exp1 > exp3)

### **Test Tuition, Subscription, and Food OP OVERLOADS**
@pytest.fixture
def tuition():
    return Tuition(5000)

@pytest.fixture
def subscription():
    return Subscription(15, "Netflix", 15.99)

@pytest.fixture
def food():
    return Food(3, "Takeout", 30)

def test_tuition_comparison(tuition):
    cheaper_tuition = Tuition(4000)
    assert cheaper_tuition < tuition  
    assert tuition > cheaper_tuition 

def test_subscription_comparison(subscription):
    cheaper_subscription = Subscription(10, "Hulu", 7.99)
    assert cheaper_subscription < subscription
    assert subscription > cheaper_subscription

def test_food_comparison(food):
    cheaper_food = Food(2, "Groceries", 10)
    assert cheaper_food < food
    assert food > cheaper_food
