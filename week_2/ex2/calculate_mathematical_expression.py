"""explanation for my choice of test values:
case 1: 2/3 vs. 1-1/3  i checked for differences between floats at the smaller decimals
case 2: check negative input
"""

def calculate_mathematical_expression(num1, num2, operation):
    if operation not in (":*+-") or (operation == ':' and num2 == 0):
        return
    if operation == "+":
        return num1 + num2
    elif operation == "-":
        return num1 - num2
    elif operation == ":":
        return num1 / num2
    elif operation == "*":
        return num1 * num2

def calculate_from_string(input):
    num1, operation, num2 = input.split()
    #cast nums
    num1 = float(num1)
    num2 = float(num2)
    return calculate_mathematical_expression(num1, num2, operation)

if __name__ == "__main__":
    calculate_mathematical_expression()
    calculate_from_string()