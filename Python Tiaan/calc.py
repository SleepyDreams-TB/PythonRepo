import math

# Function to add two numbers
def add(x, y):
    return x + y

# Function to subtract two numbers
def subtract(x, y):
    return x - y

# Function to multiply two numbers
def multiply(x, y):
    return x * y

# Function to divide two numbers
def divide(x, y):
    if y == 0:
        return "Error! Division by zero."
    return x / y

# Function for power
def power(x, y):
    return x ** y

# Function for square root
def square_root(x):
    return math.sqrt(x)

# Function for sine
def sine(x):
    return math.sin(math.radians(x))

# Function for cosine
def cosine(x):
    return math.cos(math.radians(x))

# Function for tangent
def tangent(x):
    return math.tan(math.radians(x))

# Function for logarithm (base 10)
def logarithm(x):
    return math.log10(x)

# Function for factorial
def factorial(x):
    return math.factorial(int(x))

# Main program
def scientific_calculator():
    print("Select operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Power (x^y)")
    print("6. Square root")
    print("7. Sine")
    print("8. Cosine")
    print("9. Tangent")
    print("10. Logarithm (base 10)")
    print("11. Factorial")

    # Take input from the user
    choice = input("Enter choice (1-11): ")

    # Perform the operation based on user's choice
    if choice in ['1', '2', '3', '4', '5']:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))

        if choice == '1':
            print(f"{num1} + {num2} = {add(num1, num2)}")

        elif choice == '2':
            print(f"{num1} - {num2} = {subtract(num1, num2)}")

        elif choice == '3':
            print(f"{num1} * {num2} = {multiply(num1, num2)}")

        elif choice == '4':
            print(f"{num1} / {num2} = {divide(num1, num2)}")

        elif choice == '5':
            print(f"{num1} ^ {num2} = {power(num1, num2)}")

    elif choice in ['6', '7', '8', '9', '10', '11']:
        num = float(input("Enter the number: "))

        if choice == '6':
            print(f"Square root of {num} = {square_root(num)}")

        elif choice == '7':
            print(f"Sine of {num} degrees = {sine(num)}")

        elif choice == '8':
            print(f"Cosine of {num} degrees = {cosine(num)}")

        elif choice == '9':
            print(f"Tangent of {num} degrees = {tangent(num)}")

        elif choice == '10':
            print(f"Logarithm of {num} = {logarithm(num)}")

        elif choice == '11':
            print(f"Factorial of {num} = {factorial(num)}")

    else:
        print("Invalid input")

# Run the calculator
scientific_calculator()
