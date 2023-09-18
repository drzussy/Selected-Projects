

# # # 2022 C aleph
# # lst1 = [1, 5, 2]
# # lst2 = [5, 8, 0]
# # result = [1, 6, 8]
# # ##################################

# # # Question 11


# # def sum_lists(lst1: list, lst2: list) -> list:
# #     '''take two lists representing numbers and add the two numbers and return a list representing
# #     that number)'''
# #     result = []
# #     if len(lst1) < len(lst2):
# #         smaller = lst1
# #         bigger = lst2
# #     else:
# #         smaller = lst2
# #         bigger = lst1
# #     result = [0 for i in range(len(bigger))]

# #     left_over = False
# #     for i in range(len(smaller)):
# #         if bigger[-1-i] + smaller[-1-i] >= 10:
# #             result[-1-i] += (bigger[-1-i] + smaller[-1-i] - 10)
# #             if 1+i+1 <= len(smaller):
# #                 result[-1-i-1] = 1
# #             else:
# #                 left_over = True
# #         else:
# #             result[-1-i] += bigger[-1-i] + smaller[-1-i]
# #     if left_over:
# #         if len(smaller) == len(bigger):
# #             result.insert(0, 1)
# #         else:
# #             result[-len(smaller) - 1] += 1
# #     for i in range(len(bigger) - len(smaller)):
# #         result[i] += bigger[i]

# #     return result


# # print(sum_lists(lst1, lst2))


# # def digadder(a, b, c):
# #     return (a + b + c) % 10, (a + b + c) // 10


# # def sum_lists(list_1, list_2):
# #     c = 0
# #     res = []
# #     for i in range(1, max(len(list_1), len(list_2)) + 1):
# #         a = 0 if i > len(list_1) else list_1[-i]
# #         b = 0 if i > len(list_2) else list_2[-i]
# #         x, c = digadder(a, b, c)
# #         res.insert(0, x)
# #     if c:
# #         res.insert(0, c)
# #     return res


# # print(sum_lists(lst1, lst2))
# # # 2022 C aleph
# # # 12

# class Node:
#     def __init__(self, data, prev=None, next=None):
#         self.data = data
#         self.prev: Node = prev
#         self.next: Node = next


# def cut(node):

#     p, n = node.prev, node.next.next
#     if p:
#         p.next = n
#     if n:
#         n.prev = p
#     return p if p else n


# def balanced(head):

#     while head:
#         if head.data == ')' or not head.next:
#             return False
#         if head.next.data == '(':
#             head = head.next
#         else:  # head.next.data==')'
#             head = cut(head)
#     return True


# head = Node("(")
# head.next = (Node("(", prev=head))
# head.next.next = (Node(")", prev=head.next))
# head.next.next.next = (Node("(", prev=head.next.next))
# head.next.next.next.next = (Node(")", prev=head.next.next.next))
# head.next.next.next.next.next = (Node(")", prev=head.next.next.next.next))

# print(balanced(head))


# def pairs_sum(d):
#     # convert to list of numbers
#     nums = []
#     for key in d:
#         nums += [key]*d[key]
#     nums.sort()
#     # cant divide to pairs
#     if len(nums) % 2:
#         print("not right length")
#         return False
#     # only one pair
#     if len(nums) == 2:
#         return True

#     # for every pair remove pair and find other equal pairs
#     for i in range(len(nums)):
#         for j in range(len(nums)):
#             if i == j:
#                 continue
#             temp = nums[:]
#             del temp[-i]
#             del temp[-j]
#             if find_other_pairs(temp, nums[i] + nums[j]):
#                 return True
#     return False


# def find_other_pairs(nums, value):
#     print(nums)
#     print(value)
#     if len(nums) == 0:
#         return True
#     for i in range(len(nums)):
#         for j in range(len(nums)):
#             if i == j or (nums[i] + nums[j]) != value:
#                 continue
#             temp = nums[:]
#             del temp[-i]
#             del temp[-j]
#             if find_other_pairs(temp, value):
#                 return True
#     return False


# d = {1: 2, 3: 2, 5: 2, 7: 1, 8: 1}

# print(pairs_sum(d))

# # 2022 b bet q5


# class Lnk:
#     empty = ()

#     def __init__(self, data, next=empty):
#         self.data = data
#         self.next = next

#     def __repr__(self):
#         if self.next is Lnk.empty:
#             return "Lnk({})".format(self.data)
#         else:
#             return "Lnk({}, {})".format(self.data, self.next)


# def place_between(inter, lnk_lst):
#     if lnk_lst is Lnk.empty:
#         return lnk_lst
#     if lnk_lst.next != Lnk.empty:
#         if lnk_lst.data == lnk_lst.next.data:
#             lnk_lst.next = Lnk(inter, lnk_lst.next)
#         else:
#             lnk_lst.next = place_between(inter, lnk_lst.next)
#     return lnk_lst


# print(place_between(0, Lnk.empty))
# print(place_between(-7, Lnk(-7, Lnk(3, Lnk(3)))))

# from typing import List
# from functools import reduce
# import tkinter as tki
# 65
# def no_twins(n, x, y):
#     if n == 0:
#         return [[]]
#     elif n == 1:
#         return [[x], [y]]
#     else:
#         k1, k2 = no_twins(n-1, x, y), no_twins(n-2, x, y)
#     print([[x] + d for d in k1])
#     print([[y, x] + d for d in k2])
#     return [[x] + d for d in k1] + [[y, x] + d for d in k2]


# no_twins(3, 5, 3)

# def check():
#     try:
#         print(0)
#         return 1
#     finally:
#         return 2


# print(check())


# class Tree:
#     def __init__(self, data, branches=[]):
#         self.data = data
#         self.branches = list(branches)

#     def is_a_leaf(self):
#         return not self.branches

# # 2022 b bet q 9


# def how_close(tr):
#     if tr.is_a_leaf():
#         return tr.data
#     kids_sum = 0
#     diff = []
#     for branch in tr.branches:
#         kids_sum += branch.data
#         diff.append(how_close(branch))
#     diff.append(abs(kids_sum - tr.data))
#     return min(diff)


# t1 = Tree(1, [Tree(2), Tree(3)])
# print(how_close(t1))

# t2 = Tree(7, [Tree(6), Tree(5)])
# print(how_close(t2))

# t3 = Tree(13, [Tree(8), Tree(2)])
# print(how_close(t3))

# t4 = Tree(1, [t3])
# print(how_close(t4))


# top = tki.Tk()
# buttons = [tki.Button(top, text="Button" + str(i))for i in range(3)]
# for button in buttons:
#     button.pack()


# def f(t): return lambda: print(t, end="")


# def g(x, y):
#     count = [False]

#     def foo():
#         count[0] = not count[0]
#         x() if count[0] else y()
#     return foo


# x = g(f("a"), f("b"))
# buttons[0]["command"] = f("a")
# buttons[1]["command"] = x
# buttons[2]["command"] = x
# g = g(x, f("c"))

# top.mainloop()
# from functools import reduce
# from typing import List
# print_message = True
# msg = "the product is: " if print_message else ""

# lst: List[int] = [1, -2, 0, 4, -5, 6, 0, 8, 9]
# def g(x, y): return (x if x else 1) * (y if y else 1)


# print(msg, reduce(g, lst))

lst = [1, 2, 3, 4]
print(id(lst))
lst1 = []
lst1.append(lst)
print(id(lst1[0]))
lst = [5, 6, 7, 8]
print(id(lst))
lst1.append(lst)
print(id(lst1[1]))
print(id(lst1[0]))
print(lst1)


def f(: int):
    if x < 0:
        return
    else:
        return x


g = {2: [1, "a"], 7: [3, "the", 4, "clip"]}

dict(sorted(d, lambda ))
