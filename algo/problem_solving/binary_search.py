def binary_search(elems, target):
    left, right = 0, len(elems) - 1

    while left <= right:
        middle = (left + right) // 2
        if target > elems[middle]:
            left = middle + 1
        elif target < elems[middle]:
            right = middle - 1
        else:
            return middle

    return - 1

assert(binary_search([0, 1, 2, 3, 4], 4) == 4)
assert(binary_search([0, 1, 2, 3, 4], 0) == 0)
assert(binary_search([0, 1, 2, 3, 4], 1) == 1)
assert(binary_search([0, 1, 2, 3, 4], 3) == 3)

assert(binary_search([0, 1, 2, 3, 4, 5, 6], 6) == 6)
assert(binary_search([0, 1, 2, 3, 4, 5, 6], 0) == 0)
assert(binary_search([0, 1, 2, 3, 4, 5, 6], 1) == 1)
assert(binary_search([0, 1, 2, 3, 4, 5, 6], 5) == 5)

assert(binary_search([5, 10, 15, 20, 25, 30, 35, 40, 45, 50], 5) == 0)
assert(binary_search([5, 10, 15, 20, 25, 30, 35, 40, 45, 50], 10) == 1)
assert(binary_search([5, 10, 15, 20, 25, 30, 35, 40, 45, 50], 15) == 2)
assert(binary_search([5, 10, 15, 20, 25, 30, 35, 40, 45, 50], 20) == 3)
assert(binary_search([5, 10, 15, 20, 25, 30, 35, 40, 45, 50], 25) == 4)
assert(binary_search([5, 10, 15, 20, 25, 30, 35, 40, 45, 50], 30) == 5)
assert(binary_search([5, 10, 15, 20, 25, 30, 35, 40, 45, 50], 35) == 6)
assert(binary_search([5, 10, 15, 20, 25, 30, 35, 40, 45, 50], 40) == 7)
assert(binary_search([5, 10, 15, 20, 25, 30, 35, 40, 45, 50], 45) == 8)
assert(binary_search([5, 10, 15, 20, 25, 30, 35, 40, 45, 50], 50) == 9)
