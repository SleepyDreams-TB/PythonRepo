import operator

ops = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "**": operator.pow,
    "%": operator.mod
}
'''
a = int(input("Input your first number: \n"))
op = (input("Input your Operator: \n"))
b = int(input("Input your second number: \n"))

result = ops[op](a, b)
print(result)
'''

calculation = input("Input your calculation: \n")
numbers = []
current_number = ""
operators = []

for char in calculation:
    if char.isdigit():
        current_number += char
    elif char in ops:
        if current_number != "":
            numbers.append(int(current_number))
            current_number = ""
        operators.append(char)
    elif char == " ":
        continue
    else:
        print(f"Unknown character ignored: {char}")

if current_number != "":
    numbers.append(int(current_number))

print("Operators:", operators)
print("Numbers:", numbers)

#(no precedence)
if len(numbers) == 0:
    print("No numbers entered.")
else:
    result = numbers[0]
    for i in range(len(operators)):
        op = operators[i]
        num = numbers[i + 1]
        result = ops[op](result, num)

    print("Result:", result)