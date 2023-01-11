def largest_and_smallest(val1, val2, val3):
    max_val = val1
    min_val = val2
    val_list = [val1, val2, val3]
    #iterate over maximum algor in differing order
    for i in range(len(val_list)):
        if val_list[i % 3] >= val_list[(i+1) % 3] and val_list[i % 3] >= val_list[(i+2) % 3]:
                max_val = val_list[i % 3]
    #iterate over minimum algo in differing order
    for i in range(len(val_list)):
        if val_list[i % 3] <= val_list[(i+1) % 3] and val_list[i % 3] <= val_list[(i+2) % 3]:
                min_val = val_list[i % 3]

    return max_val, min_val

def check_largest_and_smallest():
    pass_test = True
    a, b = largest_and_smallest(17, 1, 6)
    if a != 17 or b != 1:
        pass_test = False
    a, b = largest_and_smallest(1, 17, 6)
    if a != 17 or b != 1:
        pass_test = False
    a, b = largest_and_smallest(1, 1, 2)
    if a != 2 or b != 1:
        pass_test = False
    #my values
    g, h = largest_and_smallest(1-1/3, 2/3, 9)
    if a < b:
        pass_test = False
    i, j = largest_and_smallest(-90, 1, 1)
    if a == 1:
        pass_test = False
    return pass_test
largest_and_smallest(-1,10,67)
if __name__ == "__main__":
    largest_and_smallest()
    check_largest_and_smallest()