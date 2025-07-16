from CoffeeMachineClass import coffee_machine
from CoffeeMachineClass import MENU

while True:
    machine = coffee_machine()
    print("Welcome to the Coffee Machine!")
    user_input = input("Type 'Menu' to see the available options \nType 'admin' to access admin panel:\n").lower()
    
    if user_input == "admin":
        admin_input = input("To view Resource/Report of the Machine, type 'report':\nTo turn off the machine, type 'off':\n").lower()

        if admin_input == "report":
            machine.report
            continue
        elif admin_input == "off":
            print("Turning off the coffee machine.")
            break
        else:
            print(f"'{admin_input}' is an Invalid admin command.")
            continue
        
    elif user_input == 'menu':
        machine.display_menu()
        user_input = input("Please select a coffee type from the menu: ").lower()
        if user_input in MENU:
            print(machine.brewer(user_input))
            input("Press Enter to continue...")
            print("\n" * 20)
            continue
        else:
            print("Invalid coffee type. Please try again.")
            continue
    else:
        print("Invalid choice. Please try again.")
    continue
