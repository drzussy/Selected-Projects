
crawl("https://www.cs.huji.ac.il/w~intro2cs1/ex6/wiki/",
      "week_6\small_index.txt", "out_file")
with open('out2.pickle', 'wb')as f:
    print(pickle.load(f))


test_dict = {'a': {'b': 1, 'c': 3, 'd': 4, 'e': 5},
             'f': {'g': 1, 'h': 2, 'i': 3}}
print(test_dict['a']['e'])
print(count_total_refrences(test_dict, "f"))

mentions = {"harry": {"hermione": 1, "malfoy": 1}, "malfoy": {
    "harry": 1}, "hogwarts": {"harry": 1}, "hermione": {}}
rankings = {"harry": 1, 'hermione': 1, 'malfoy': 1, 'hogwarts': 1}
# create new rankings dictionary
new_rankings = {"harry": 0, 'hermione': 0, 'malfoy': 0, 'hogwarts': 0}
for link in mentions:
    total_refrences = count_total_refrences(mentions, link)
    for refrenced in mentions[link]:
        new_rankings[refrenced] += rankings[link] * \
            (mentions[link][refrenced] / total_refrences)
print(new_rankings)

search() tests
crawl("https://www.cs.huji.ac.il/w~intro2cs1/ex6/wiki/",
      "week_6\small_index.txt", "out_file1")
page_rank(100, "out_file1", "out_file2")
words_dict("https://www.cs.huji.ac.il/w~intro2cs1/ex6/wiki/",
           "week_6\small_index.txt", "out_file3")
search("scar", "out_file2", "out_file3", 4)
search("Crookshanks", "out_file2", "out_file3", 4)
search("Horcrux", "out_file2", "out_file3", 4)
search("Pensieve McGonagall", "out_file2", "out_file3", 4)
search("broom wand cape", "out_file2", "out_file3", 4)

pages_with_query() tests

test_dict = {"scar": {"harry.html": 0, "hermione.html": 1, "ron.html": 1},
             "broom": {"harry.html": 0, "ron.html": 1}, }
rankings = {"harry.html": 1, "ron.html": 10,
            "hermione.html": 20, "albus.html": 4}
print(pages_with_query(["is", "scar", "from",
      "broom", "accident"], rankings, test_dict))
