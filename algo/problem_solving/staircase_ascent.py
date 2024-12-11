def staircase_ascent(steps_count, current_step):
    if n == 0 or current_step == steps_count:
        return 1
    elif current_step > steps_count:
        return 0

    return staircase_ascent(steps_count, current_step + 1) + staircase_ascent(steps_count, current_step + 2) + staircase_ascent(steps_count, current_step + 3)

def staircase_ascent_frontend(steps_count):
    return staircase_ascent(steps_count, 0)

print(staircase_ascent_frontend(35))