def num_permutations(word):
    count = [0]
    permute(list(word), 0, len(word), count)
    return count[0]


def permute(string, l, r, count):
    if l == r:
        print(string)
        count[0] += 1
    else:
        for i in range(l, r):
            string[l], string[i] = string[i], string[l]
            permute(string, l + 1, r, count)
            string[l], string[i] = string[i], string[l]


num_permutations("abc")

# def foo(n):
#     if n <= 0:
#         return
#     x = 0
#     for i in range(n):
#         x += 0.1
#     return foo(n // 2)


# foo(49)

# def aggragate(func):
#     answers = []

#     def new_func(x):
#         answers.append(func(x))
#         print(answers)
#     return new_func


# @aggragate
# def f(x): return x*2


# g = aggragate(lambda x: x/2)

# f(5)
# f(2)
# g(10)
# g(20)
# f(3)

lst = [0, 1, '2', 3, 'a']
for element in lst:
    try:
        print(6//int(element), end=" ")
    except ValueError:
        print("oops", end=" ")
    except ZeroDivisionError:
        print("Boom", end=" ")
