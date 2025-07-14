def isdigit(var):
    if type(var) == int:
        is_digit = True
    else:
        is_digit = False
    return is_digit

str_num = 'A'
num = int(str_num)
print(isdigit(num))