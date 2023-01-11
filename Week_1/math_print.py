import math

def golden_ratio():
    print((1+math.sqrt(5))/2)

def six_squared():
    print(6**2)

def hypotenuse():
    print(math.hypot(12,5))

def pi():
    print(math.pi)

def e():
    print(math.e)

def squares_area():
    for i in range(9):
        print(int(math.pow((i+1),2)), end=' ')
    print(100)

if __name__ == '__main__':
    golden_ratio()
    six_squared()
    hypotenuse()
    pi()
    e()
    squares_area()