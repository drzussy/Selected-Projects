

def all_permutations(lst):
    _all_perm_helper(lst, 0)


def _all_perm_helper(lst, ind):
    if ind == len(lst) - 1:
        print(lst)
        return

    _all_perm_helper(lst, ind + 1)
    for i in range(ind + 1, len(lst)):
        lst[ind], lst[i] = lst[i], lst[ind]
        _all_perm_helper(lst, ind+1)
        lst[ind], lst[i] = lst[i], lst[ind]


# all_permutations([1, 2, 3])
