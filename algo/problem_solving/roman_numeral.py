mappings = {
    1000: "M",
    900: "CM",
    500: "D",
    400: "CD",
    100: "C",
    90: "XC",
    50: "L",
    40: "XL",
    10: "X",
    9: "IX",
    5: "V",
    4: "IV",
    1: "I",
}

def convert_to_roman_iter(num):
    result = []

    while num != 0:
        for n, m in mappings.items():
            if num - n >= 0:
                result.append(m)
                num -= n
                break

    return ''.join(result)


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