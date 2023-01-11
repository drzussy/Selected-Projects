##############################################
#               Tester for ex11              #
##############################################
# Move ALL files to the same folder with ex11#
# then run pytest                            #
# Daniel Shookroun                           #
# daniel.shookroun@mail.huji.ac.il           #
##############################################

import ex11
from ex11 import Node, Diagnoser, Record, build_tree, optimal_tree, parse_data

# Manually build a simple tree.
#                cough
#          Yes /       \ No
#        fever           healthy
#   Yes /     \ No
# influenza   cold

flu_leaf = Node("influenza", None, None)
cold_leaf = Node("cold", None, None)
inner_vertex = Node("fever", flu_leaf, cold_leaf)
healthy_leaf = Node("healthy", None, None)
root = Node("cough", inner_vertex, healthy_leaf)

diagnoser = Diagnoser(root)

flu_leaf2 = Node("influenza", None, None)
cold_leaf2 = Node("cold", None, None)
hard_leaf2 = Node("hard influenza", None, None)
headache_node2 = Node("headache", hard_leaf2, flu_leaf2)
inner_vertex2 = Node("fever", headache_node2, cold_leaf2)
healthy_leaf2 = Node("healthy", None, None)
root2 = Node("cough", inner_vertex2, healthy_leaf2)

diagnoser2 = Diagnoser(root2)
# Manually build of diagnoser2.
#                          cough
#                    Yes /       \ No
#                  fever           healthy
#             Yes /     \ No
#            headache   cold
#       Yes /     \ No
# hard influenza influenza

flu_leaf3 = Node("influenza", None, None)
cold_leaf3 = Node("cold", None, None)
hard_leaf3 = Node("hard influenza", None, None)
headache_node3 = Node("headache", hard_leaf3, flu_leaf3)
inner_vertex3 = Node("fever", headache_node3, cold_leaf3)
healthy_leaf3 = Node("hard influenza", None, None)
root3 = Node("cough", inner_vertex3, healthy_leaf3)

diagnoser3 = Diagnoser(root3)
# Manually build of diagnoser3.
#                          cough
#                    Yes /       \ No
#                  fever       hard influenza
#             Yes /     \ No
#            headache   cold
#       Yes /     \ No
# hard influenza influenza

flu_leaf4 = Node("influenza", None, None)
cold_leaf4 = Node("cold", None, None)
hard_leaf4 = Node("hard influenza", None, None)
headache_node4 = Node("headache", hard_leaf4, flu_leaf4)
inner_vertex4 = Node("fever", headache_node4, cold_leaf4)
healthy_leaf4 = Node("influenza", None, None)
root4 = Node("cough", inner_vertex4, healthy_leaf4)

diagnoser4 = Diagnoser(root4)
# Manually build of diagnoser4.
#                          cough
#                    Yes /       \ No
#                  fever        influenza
#             Yes /     \ No
#            headache   cold
#       Yes /     \ No
# hard influenza influenza

flu_leaf5 = Node("influenza", None, None)
cold_leaf5 = Node("cold", None, None)
healthy_leaf5 = Node("influenza", None, None)
inner_vertex6 = Node("headache", cold_leaf5, healthy_leaf5)
inner_vertex5 = Node("headache", flu_leaf5, cold_leaf5)
root5 = Node("cough", inner_vertex5, inner_vertex6)

diagnoser5 = Diagnoser(root5)
# Manually build of diagnoser5.
#                          cough
#                    Yes /       \ No
#                     headache  headache
#             Yes /     \ No  Yes /     \ No
#           influenza  cold     cold    healthy

root6 = Node("cold", None, None)
diagnoser6 = Diagnoser(root6)




def test_diagnose1():
    assert "cold" == diagnoser.diagnose(["cough"])


def test_diagnose2():
    assert "influenza" == diagnoser2.diagnose(["cough", "fever"])


def test_success_rate1():
    records = [Record("influenza", ["cough", "fever"]), Record("healthy", []),
               Record('hard influenza', ["cougth", "fever", "headache"])]
    assert 0.6666666666666666 == diagnoser.calculate_success_rate(records)


def test_success_rate2():
    records2 = [Record("influenza", ["cough", "fever"]), Record("healthy", []),
                Record('hard influenza', ["cough", "fever", "headache"])]
    assert 1.0 == diagnoser2.calculate_success_rate(records2)


def test_success_rate3():
    records3 = [Record("influenza", ["cough", "fever"]),
                Record("indigestion", ["stomachache"])]
    assert 0.5 == diagnoser2.calculate_success_rate(records3)


def test_all_illnesses1():
    result = diagnoser3.all_illnesses()
    assert "hard influenza" == result[0]

def test_all_illnesses_and_build_tree():
    symptoms = []
    records = parse_data("test_all_illnesses.txt")
    for record in records:
        for symptom in record.symptoms:
            if symptom not in symptoms:
                symptoms.append(symptom)
    assert build_tree(records, symptoms).all_illnesses() == ["influenza", "cold", "strep", "mono", "healthy"], f"""the output from the function all_illnesses should not be:\n{build_tree(records, symptoms).all_illnesses()}\nbut: ["influenza", "cold", "strep", "mono", "healthy"]\nthe diagnoser was built by the function built_tree with the records taken from test_all_illnesses.txt"""



def test_paths_to_illness1():
    paths1 = diagnoser4.paths_to_illness('influenza')
    assert [[True, True, False], [False]] == paths1 or [[False], [True, True, False]] == paths1


def test_paths_to_illness2():
    paths2 = diagnoser4.paths_to_illness('cold')
    assert [[True, False]] == paths2


def test_paths_to_illness3():
    paths3 = diagnoser4.paths_to_illness('something_that_doesnt_exist')
    assert [] == paths3


def test_paths_to_illness4():
    paths4 = diagnoser6.paths_to_illness("cold")
    assert [] == paths4 or [[]] == paths4


def test_paths_to_illness5():
    paths5 = diagnoser2.paths_to_illness('healthy')
    assert [[False]] == paths5


def test_paths_to_illness6():
    paths6 = diagnoser5.paths_to_illness('cold')
    assert [[True, False], [False, True]] == paths6 or [[False, True], [True,
                                                                        False]] == paths6

def test_paths_to_illnesses_and_build_tree():
    paths = [[], [[False, False, False, False, False, False, False, False, False, False, False, False, False, False]], [[True, True, False, False, False, False, False, False, False, False, False, False, False, False], [True, False, False, False, False, False, False, False, False, False, False, False, False, False]], [[False, False, True, True, True, False, False, False, False, False, False, False, False, False], [False, False, True, True, False, False, False, False, False, False, False, False, False, False], [False, False, True, False, False, False, False, False, False, False, False, False, False, False]], [[False, False, False, False, False, True, True, True, True, False, False, False, False, False], [False, False, False, False, False, True, True, True, False, False, False, False, False, False], [False, False, False, False, False, True, True, False, False, False, False, False, False, False], [False, False, False, False, False, True, False, False, False, False, False, False, False, False]], [[False, False, False, False, False, False, False, False, False, True, True, True, True, True], [False, False, False, False, False, False, False, False, False, True, True, True, True, False], [False, False, False, False, False, False, False, False, False, True, True, True, False, False], [False, False, False, False, False, False, False, False, False, True, True, False, False, False], [False, False, False, False, False, False, False, False, False, True, False, False, False, False]]]
    symptoms = []
    illnesses = []
    records = parse_data("test_all_illnesses.txt")
    for record in records:
        for symptom in record.symptoms:
            if symptom not in symptoms:
                symptoms.append(symptom)
        if record.illness not in illnesses:
            illnesses.append(record.illness)
    diagno = build_tree(records, symptoms)
    for i in range(len(paths)):
        assert diagno.paths_to_illness(illnesses[i]) == paths[i], f"the paths to the illness {illnesses[i]} \nis not: {diagno.paths_to_illness(illnesses[i])} \nbut: {paths[i]}\nthe diagnoser was built by the function built_tree with the records taken from test_all_illnesses.txt"


def test_build_tree1():
    records = parse_data("tiny_data2.txt")
    tree1 = build_tree(records, ["headache", "fever"]).root

    assert "meningitis" == tree1.positive_child.positive_child.data
    assert "influenza" == tree1.positive_child.negative_child.data
    assert "cold" == tree1.negative_child.positive_child.data
    assert "healthy" == tree1.negative_child.negative_child.data


def test_build_tree2():
    records = parse_data("small_data1.txt")
    tree2 = build_tree(records, ["headache", "fever"]).root

    assert "influenza" == tree2.positive_child.positive_child.data
    assert "cold" == tree2.positive_child.negative_child.data
    assert "strep" == tree2.negative_child.positive_child.data
    assert "healthy" == tree2.negative_child.negative_child.data


def test_build_tree3():
    records = parse_data("medium_data1.txt")
    tree3 = build_tree(records, ["fever", "cough"]).root

    assert "influenza" == tree3.positive_child.positive_child.data
    assert "meningitis" == tree3.positive_child.negative_child.data
    assert "cold" == tree3.negative_child.positive_child.data
    assert "healthy" == tree3.negative_child.negative_child.data


def test_build_tree4():
    records = parse_data("medium_data2.txt")
    tree4 = build_tree(records, ["fever", "cough"]).root

    assert "influenza" == tree4.positive_child.positive_child.data
    assert "strep" == tree4.positive_child.negative_child.data
    assert "cold" == tree4.negative_child.positive_child.data
    assert "healthy" == tree4.negative_child.negative_child.data


def test_optimal_tree1():
    records = parse_data("test_optimal_tree1.txt")
    tree = optimal_tree(records, ["cough", "fever", "headache"], 2).root

    assert "cough" == tree.data or "fever" == tree.data
    assert "cough" == tree.positive_child.data or "fever" == tree.positive_child.data


def test_optimal_tree2():
    records = parse_data("test_optimal_tree2.txt")
    tree = optimal_tree(records, ["cough", "fever", "headache"], 1).root

    assert "fever" == tree.data or "headache" == tree.data


def test_optimal_tree3():
    records = parse_data("test_optimal_tree3.txt")
    tree = optimal_tree(records, ["fever", "cough", "headache"], 2).root

    assert "influenza" == tree.positive_child.positive_child.data
    assert "meningitis" == tree.positive_child.negative_child.data
    assert "cold" == tree.negative_child.positive_child.data
    assert "healthy" == tree.negative_child.negative_child.data

def test_7():
    def print_in_order(diagno: Diagnoser):
        printable = ['']

        def print_in_order_helper(cur_node: Node):
            if cur_node is None:
                return
            if cur_node.positive_child:
                print_in_order_helper(cur_node.positive_child)
            printable[0] += str(cur_node.data) + ' '
            if cur_node.negative_child:
                print_in_order_helper(cur_node.negative_child)

        print_in_order_helper(diagno.root)
        return printable[0][:-1]

    def check(n: Node):
        def helper(a, b):
            if not a and not b:
                return True
            if not a or not b:
                return False
            if a.data != b.data:
                return False
            if helper(a.positive_child, b.positive_child):
                return helper(a.negative_child, b.negative_child)
            return False

        if n.positive_child is None:
            return False
        return helper(n.positive_child, n.negative_child)

    def check_for_nones(cur_root: Node):
        if cur_root is None:
            return False
        if cur_root.data is None:
            return True
        if cur_root.positive_child:
            is_there_none_in_pos = check_for_nones(cur_root.positive_child)
            is_there_none_in_neg = check_for_nones(cur_root.negative_child)
            return is_there_none_in_pos or is_there_none_in_neg
        return False



    files = ["tiny_data.txt", "tiny_data2.txt", "small_data.txt", "small_data1.txt", "medium_data.txt", "medium_data1.txt", "medium_data2.txt", "big_data.txt", "test_optimal_tree1.txt", "test_optimal_tree2.txt", "test_optimal_tree3.txt"]

    rates_built_tree = [1.0, 1.0, 0.9333333333333333, 0.9333333333333333, 0.9083333333333333, 0.9459459459459459, 0.9501133786848073, 0.9156666666666666, 1.0, 1.0, 1.0]
    rates_optimal = [[0.16666666666666666, 0.25, 0.16666666666666666, 0.16666666666666666, 0.16666666666666666, 0.22358722358722358, 0.26077097505668934, 0.16666666666666666, 0.25, 0.5, 0.25], [0.3333333333333333, 0.5, 0.3333333333333333, 0.3333333333333333, 0.325, 0.40540540540540543, 0.4467120181405896, 0.32516666666666666, 0.5, 1.0, 0.5], [0.6666666666666666, 1.0, 0.6, 0.6, 0.5766666666666667, 0.6781326781326781, 0.7029478458049887, 0.5598333333333333, 1.0, 1.0, 1.0]]
    list_of_rates = [rates_optimal[0], rates_optimal[1], rates_optimal[2],
                     rates_built_tree]
    for i in range(len(list_of_rates)):
        rates = list_of_rates[i]
        for ind, file in enumerate(files):
            symps = []
            r = parse_data(file)
            for record in r:
                for s in record.symptoms:
                    if s not in symps:
                        symps.append(s)
            if i < len(list_of_rates) - 1:
                diagnoser = optimal_tree(r, list(symps), i)
            else:
                symps += [symps[0]]
                diagnoser = build_tree(r, list(symps))
            rate_before_minimizing = diagnoser.calculate_success_rate(r)
            diagnoser.minimize(False)
            assert check(diagnoser.root) == False, f"your minimize(False) function dos not remove all duplications!\nfile name: {file},\nthe tree was built using the optimal_tree function with a depth of {i}" if i < 3 else f"your minimize(False) function dos not remove all duplications!\nfile name: {file},\nthe tree was built using the built_tree function"
            rate_after_removing_duplications = diagnoser.calculate_success_rate(r)
            diagnoser.minimize(True)
            assert check_for_nones(diagnoser.root) == False, f"your minimize(True) dos not remove all nones!\nfile name: {file},\nthe tree was built using the optimal_tree function with a depth of {i}" if i < 3 else f"your minimize(True) dos not remove all nones!\nfile name: {file},\nthe tree was built using the built_tree function"
            rate_after_removing_empties = diagnoser.calculate_success_rate(r)
            assert rate_before_minimizing == rate_after_removing_duplications, f"your minimize(False) function changes the rate of success of the diagnoser, it should not do that!\nbefore: {rate_before_minimizing}, after: {rate_after_removing_duplications}\nfile name: {file},\nthe tree was built using the optimal_tree function with a depth of {i}" if i < 3 else f"your minimize(False) function changes the rate of success of the diagnoser, it should not do that!\nbefore: {rate_before_minimizing}, after: {rate_after_removing_duplications}\nfile name: {file},\nthe tree was built using the built_tree function"
            assert rate_after_removing_duplications == rate_after_removing_empties, f"your minimize(True) function changes the rate of success of the diagnoser, it should not do that!\nbefore: {rate_after_removing_duplications}, after: {rate_after_removing_empties}\nfile name: {file},\nthe tree was built using the optimal_tree function with a depth of {i}" if i < 3 else f"your minimize(True) function changes the rate of success of the diagnoser, it should not do that!\nbefore: {rate_after_removing_duplications}, after: {rate_after_removing_empties}\nfile name: {file},\nthe tree was built using the built_tree function"
            assert rate_after_removing_empties == rates[ind], f"the rate you calculated dos not mach the rate we have in our data\nyour rate: {rate_before_minimizing}, our rate: {rate_after_removing_duplications}\nfile name: {file},\nthe tree was built using the optimal_tree function with a depth of {i}" if i < 3 else f"the rate you calculated dos not mach the rate we have in our data\nyour rate: {rate_before_minimizing}, our rate: {rate_after_removing_duplications}\nfile name: {file},\nthe tree was built using the built_tree function"


