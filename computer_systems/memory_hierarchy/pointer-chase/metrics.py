import csv
import math
import time

def average_age(ages):
    total = 0
    for age in ages:
        total += age

    return total / len(ages)

def average_payment_amount(payments):
    amount = 0
    count = len(payments)

    for dollars, cents in payments:
        amount += dollars + cents / 100

    return amount / count


def stddev_payment_amount(payments, mean):
    squared_diffs = 0
    count = len(payments)

    for dollars, cents in payments:
        amount = dollars + cents / 100
        diff = amount - mean
        squared_diffs += diff * diff

    return math.sqrt(squared_diffs / count)


def load_data():
    users_ages = []
    users_payments = []

    with open('users.csv') as f:
        for line in csv.reader(f):
            _, _, age, _, _ = line
            users_ages.append(int(age))
    with open('payments.csv') as f:
        for line in csv.reader(f):
            amount, _, _ = line
            dollars = float(int(amount)//100)
            cents = float(amount) % 100
            users_payments.append((dollars, cents))

    return users_ages, users_payments

if __name__ == '__main__':
    t = time.perf_counter()
    ages, payments = load_data()
    print(f'Data loading: {time.perf_counter() - t:.3f}s')
    t = time.perf_counter()
    assert abs(average_age(ages) - 59.626) < 0.01

    avg_payments_amount = average_payment_amount(payments)
    assert abs(avg_payments_amount - 499850.559) < 0.01

    assert abs(stddev_payment_amount(payments, avg_payments_amount) - 288684.849) < 0.01
    print(f'Computation {time.perf_counter() - t:.3f}s')
