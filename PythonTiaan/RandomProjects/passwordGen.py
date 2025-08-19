import random

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
cases = [0,0,1,1,2]

exit = False

while not exit:
  try:

    print("Welcome to the PyPassword Generator!")
    nr_chars = int(input("Password Length?\n"))
    include_symbols = bool(input(f"Would you like symbols? (Type True or False)\n"))
    include_numbers = bool(input(f"Would you like numbers? (Type True or False)\n"))
    preset = bool(input("Would you like to remove hard to read characters such as ['o', 'i', '0', 'l'] ? (Type True or False)\n"))
    exclude = list(input("What would you like to exclude?: "))
    print(exclude)

    if preset:
      letters.pop(letters.index('o'))
      letters.pop(letters.index('i'))
      letters.pop(letters.index('l'))
      numbers.pop(numbers.index('0'))

    for i in range(0, (len(exclude))):
      if exclude[i] in letters:
        letters.pop(letters.index(exclude[i]))
      elif exclude[i] in numbers and include_numbers:
        numbers.pop(numbers.index(exclude[i]))
      elif exclude[i] in symbols:
        symbols.pop(symbols.index(exclude[i]))
      else:
        continue    
      
    password = ""
    i = 0

    for i in range(0, (nr_chars + 1)):
        char_type =+ random.choice(range(0, (len(cases))))
        if char_type == 0:
          password += random.choice(letters)
        elif char_type == 1 and include_numbers:
          password += random.choice(numbers)
        elif char_type == 2 and include_symbols:
          password += random.choice(symbols)

    gen_password = list(password)
    random.shuffle(gen_password)
    password = "".join(gen_password)
    print("Generated Password:", password)
    prompt = input("Woud you like to generate another password ? Type 'y' for yes and 'n' for no:\n")

    if prompt == 'y':
      continue
    else:
      exit = False
      print("Goodbye")
  except ValueError:
    print("Invalid Input, the program will now restart")