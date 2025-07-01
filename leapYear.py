
def is_leap_year(year):
    result = False

    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                result = True
        else:
            result = True
    else:
        result = False
    return result

year = int(2020)
print(is_leap_year(year))