def all_permutations(lst):
    result = []
    _all_perm_helper(lst, result, 0)
    return result


def _all_perm_helper(lst, result, ind):
    if ind == len(lst) - 1:
        result.append(lst[:])  # copy the lists (why the [:]?)
        return

    _all_perm_helper(lst, result, ind + 1)
    for i in range(ind + 1, len(lst)):
        lst[ind], lst[i] = lst[i], lst[ind]
        _all_perm_helper(lst, result, ind+1)
        lst[ind], lst[i] = lst[i], lst[ind]
