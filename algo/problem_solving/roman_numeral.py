mappings = {
    1: "I",
    4: "IV",
    5: "V",
    9: "IX",
    10: "X",
    40: "XL",
    50: "L",
    90: "XC",
    100: "C",
    400: "CD",
    500: "D",
    900: "CM",
    1000: "M"
}

def convert_to_roman_iter(num):
    result = ""

    while num != 0:
        m = max([n for n in mappings if num - n >= 0])
        num -= m
        result += mappings[m]

    return result


def convert_to_roman_recursive(num):
    if num == 0:
        return ""

    m = max([n for n in mappings if num - n >= 0])

    return mappings[m] + convert_to_roman_recursive(num - m)

assert(convert_to_roman_recursive(250) == "CCL")
assert(convert_to_roman_recursive(5) == "V")
assert(convert_to_roman_recursive(1025) == "MXXV")
assert(convert_to_roman_recursive(29) == "XXIX")
assert(convert_to_roman_recursive(2421) == "MMCDXXI")

assert(convert_to_roman_iter(250) == "CCL")
assert(convert_to_roman_iter(5) == "V")
assert(convert_to_roman_iter(1025) == "MXXV")
assert(convert_to_roman_iter(29) == "XXIX")
assert(convert_to_roman_iter(2421) == "MMCDXXI")