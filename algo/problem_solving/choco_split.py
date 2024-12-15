def choco_split_iterative(n, m):
    bars_count = 0

    while n != 0:
        bars_count += m
        n -= 1

    return bars_count - 1

def choco_split_recursive(n, m):
    if m == 1:
        return n - 1

    return 1 + choco_split_recursive(n, m - 1) + choco_split_recursive(n, 1)

def choco_split_formula(n, m):
    return (n * m) - 1


# Tests
assert(choco_split_formula(4, 3) == 11)
assert(choco_split_formula(4, 2) == 7)
assert(choco_split_formula(3, 3) == 8)
assert(choco_split_formula(3, 6) == 17)

assert(choco_split_iterative(4, 3) == 11)
assert(choco_split_iterative(4, 2) == 7)
assert(choco_split_iterative(3, 3) == 8)
assert(choco_split_iterative(3, 6) == 17)

assert(choco_split_recursive(4, 3) == 11)
assert(choco_split_recursive(4, 2) == 7)
assert(choco_split_recursive(3, 3) == 8)
assert(choco_split_recursive(3, 6) == 17)
