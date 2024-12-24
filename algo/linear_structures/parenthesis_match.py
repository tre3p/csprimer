mappings = {
    ")": "(",
    "]": "[",
    "}": "{",
}


def parenthesis_match(str):
    seen = []

    for p in str:
        if p in mappings.values():  # if current char is opening bracket - just append it to the stack
            seen.append(p)
        elif p in mappings.keys():  # if current char is closing bracket - check if previously opened bracket was of matching type
            if len(seen) == 0 or seen.pop() != mappings[p]:
                return False

    return len(seen) == 0


assert (parenthesis_match("()") == True)
assert (parenthesis_match("[{()}]") == True)
assert (parenthesis_match("[{()(())}]") == True)

assert (parenthesis_match("[)") == False)
assert (parenthesis_match("[") == False)
assert (parenthesis_match("}") == False)
assert (parenthesis_match("(([{}])") == False)
assert (parenthesis_match("[{(]}]") == False)
