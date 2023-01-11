def is_vormir_safe(min, day1, day2, day3):
    list = [day1, day2, day3]
    counter = 0
    for i in range(3):
        if list[i] > min:
            counter += 1
    if counter > 1:
        return True
    else:
        return False
if __name__ == "__main__":
    is_vormir_safe()