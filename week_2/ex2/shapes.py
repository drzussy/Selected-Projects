import math

def shape_area():
    user_input = input("Choose shape (1=circle, 2=rectangle, 3=triangle): ")
    #check legal user input
    if user_input not in ("123"):
        return
    if user_input == '1': #calculate area of circle
        radius = int(input())
        return math.pi * radius ** 2
    elif user_input == '2': #calculate area of rectangle
        a = int(input())
        b = int(input())
        return a * b
    else: #calculate area of triangle
        side = int(input())
        return (3**0.5/4) * side**2

if __name__ == "__main__":
    shape_area()