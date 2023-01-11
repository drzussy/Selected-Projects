
def quadratic_equation(a, b, c):
    disci = b ** 2 - 4 * a * c
    if disci < 0:
        return None, None
    if disci == 0:
        return -b/(2 * a), None
    if disci > 0:
        return (-b + disci ** 0.5) / (2 * a), (-b - disci ** 0.5) / (2 * a)

def quadratic_equation_user_input():
    user_input = input("Insert coefficients a, b, and c: ")
    a, b, c = user_input.split()

    if int(a) == 0:
        print("The parameter 'a' may not equal 0")
        return
    res1, res2 = quadratic_equation(int(a),int(b),int(c))
    ans1 = str(res1)
    ans2 = str(res2)
    if res1 and res2:
        print("The equation has 2 solutions: " + ans1 + " and " + ans2)
    elif res2 or res1:
        if res2:
            print("The equation has 1 solution: " + ans2)
        else:
            print("The equation has 1 solution: " + ans1)
    if not res1 and not res2:
        print("The equation has no solutions" )

if __name__ == "__main__":
    quadratic_equation()
    quadratic_equation_user_input()
