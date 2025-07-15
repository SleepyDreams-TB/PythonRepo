MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

class coffee_machine:
  
  def __init__(self):
        self.profit = 0

  def report(self):
    print("--------------------------------------")
    print("COFFEE MACHINE REPORT:")
    print("--------------------------------------")
    print(f"Current profit: ${self.profit:.2f}")
    print("Resources report:")
    for resource, amount in resources.items():
        print(f"{resource.title()}: {amount}ml")
    user_input = input("Would you like to refill resources? (yes/no): ").lower()
    if user_input == "yes":    
      ingredient = input("What would you like to refill? (Coffee/Milk/Water)").lower()
      if ingredient in resources:
          mili = int(input("How much Would you like to add? *Max 1000ml each*"))
          if ((mili + resources[ingredient]) <= 1000):
            resources[ingredient] += mili
            print(f"{mili}ml of {ingredient} successfully added to resources")
            print(f"Current Stock of {ingredient}: {resources[ingredient]}")
          else:
            print("Input too Large Maximum Capacity Reached.")
            remainder = (mili +resources[ingredient]) - 1000
            print(f"Excess returned: {remainder}")
            resources[ingredient] = 1000
      else:
          print("Invalid Input.")
          return
  
  def display_menu(self):
    print("--------------------------------------")
    print("Menu:")
    print("--------------------------------------")
    for coffee, details in MENU.items():
      print(f"{coffee.title()}: ${details['cost']}")

  def payment(self, coffee_type):
    cost = MENU[coffee_type]["cost"]
    deposit = float(input(f"Please insert ${cost} for your {coffee_type}."))
    if deposit < cost:
        return "Not enough money. Please insert more."
    elif deposit >= cost:
        change = deposit - cost
        print(f"Here is your change: ${change:.2f}")
        self.profit += cost
    return True

  def brewer(self, coffee_type):
    if coffee_type in MENU:
        ingredients = MENU[coffee_type]["ingredients"]
        for item, amount in ingredients.items():
            if resources[item] < amount:
                return f"Resources: Sorry, not enough {item}."
            if self.payment(coffee_type):
                resources[item] -= amount
                return(f"Here is your {coffee_type}!")
            else:
                return "Payment failed. Insufficient Deposit. Please try again."
        else:
            return "Invalid coffee type."