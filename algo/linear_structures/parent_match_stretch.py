bracket_mappings = {
    ")": "(",
    "]": "[",
}

def validate_lisp_brackets(file_name):
    # format: (bracket, line, pos in line)
    seen = []

    with (open(file_name, "r")) as file:
        for line_num, line in enumerate(file, 1):
            for char_num, char in enumerate(line):
                if char in bracket_mappings.values(): # if it's opening bracket - put it to the stack
                    seen.append((char, line_num, char_num))
                elif char in bracket_mappings.keys(): # if it's closing bracket - validate if it was opened correctly
                    if len(seen) == 0:
                        print_redundant_bracket_err(char, line_num, char_num)
                        return
                    open_bracket_char, open_bracket_l_num, open_bracket_c_num = seen.pop()
                    if bracket_mappings[char] != open_bracket_char:
                        print_err(open_bracket_char, open_bracket_l_num, open_bracket_c_num, line_num, char_num)
                        return
                elif char == ';': # if it's comment - skip this line
                    break

    if len(seen) != 0:
        print("Errors detected:")
        for (br, open_line, char_num) in seen: print_unclosed_bracket_err(br, open_line, char_num)

def print_unclosed_bracket_err(bracket, line_num, char_num):
    print(f"Bracket '{bracket}' was opened, but never closed. Line: {line_num}, pos: {char_num}")

def print_redundant_bracket_err(bracket, line_num, char_num):
    print(f"Redundant closing bracket '{bracket}' at line {line_num}, position {char_num}")

def print_err(bracket, open_line, open_pos, closing_line, closing_pos):
    print(f"Bracket '{bracket}' opened at line {open_line}, position {open_pos}, but wasn't closed. Should be closed at line {closing_line}, position {closing_pos}")

validate_lisp_brackets("stretch.rkt")