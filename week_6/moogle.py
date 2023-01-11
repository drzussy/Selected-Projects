import argparse
import collections
import urllib.parse
import requests
import bs4
import pickle
import sys


def mentions_counter(index_file):
    '''Create a dictionary so that for every link in index file a key:vale pair of link:0 is added. '''
    with open(index_file, 'r') as f:
        # create a dict of links
        links = {}
        for link in f:
            links.update({link.strip(): 0})
        f.close()
    return links


def get_html_page_soup(base_url, link):
    '''gets html and turns into soup'''
    response = requests.get(urllib.parse.urljoin(base_url, link))
    html = response.text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    return soup


def count_mentions(base_url, f, index_file):
    '''counts mentions of '''
    traffic_dict = {}
    for link in f:
        link = link.strip()
        # for each link add key in traffic_dict
        traffic_dict.update({link: {}})
        # create the value for traffic_dict[link]
        links_dic = mentions_counter(index_file)
        # get page html soup
        soup = get_html_page_soup(base_url, link)
        # add 1 for each mention of link in links dictionary
        for p in soup.find_all("p"):
            for a in p.find_all("a"):
                mentioned_link = a.get("href")
                if mentioned_link in links_dic:
                    links_dic[mentioned_link] += 1
        # make sure there arent any 0 values
        for page in links_dic:
            if links_dic[page] != 0:
                traffic_dict[link][page] = links_dic[page]
        # add results to traffic_dict
        # traffic_dict[link] = links_dic
    return traffic_dict


def crawl(base_url: str, index_file: str, out_file: str):
    '''creates a dictionary that contains amount of link mentions on one webpage'''
    with open(index_file, 'r') as f:
        # create traffic_dict[page name, Dict[linked page name, number of mentions]]
        traffic_dict = count_mentions(base_url, f, index_file)
        f.close()
    # save traffic_dict as pickle file
    with open(out_file, 'wb') as g:
        pickle.dump(traffic_dict, g)
    return


def make_dict_of_links(mentions, default_val):
    '''Iterate over mentions and create a dictionary of all the links with values of default_val'''
    new_r = {}
    for key in mentions:
        new_r[key] = default_val
    return new_r


def count_total_refrences(mentions: dict, link) -> int:
    '''count total amount of refrences for a key value in mentions'''
    sum_total = sum(mentions[link].values())
    return sum_total


def update_rankings(mentions: dict, rankings: dict) -> dict:
    '''Iterate over all the links in the key values of mention and update the rankings of all the links based on the mentions inside links' webpage'''
    new_rankings = make_dict_of_links(mentions, 0)
    # iterate over all links
    for link in mentions:
        total_refrences = count_total_refrences(mentions, link)
        # for each refrenced in link, update refrenced rankings based on current link mentions
        for refrenced in mentions[link]:
            new_rankings[refrenced] += rankings[link] * \
                (mentions[link][refrenced] / total_refrences)
    return new_rankings


def page_rank(iterations, dict_file, out_file):
    '''Rank a list of links based on the number of mentiones to each other. Variables: iterations = number of times to func_to_run ranking algorithm; dict_file = A pickle file that contains a dictionary of the links where each value is a dictionary that contains the number of mentions to the links in the key values of the overall dictionary; out_file = name of pickle file that is returned'''
    with open(dict_file, 'rb') as f:
        mentions = pickle.load(f)
        # default rankings
        rankings = make_dict_of_links(mentions, 1)
        # go through iterations
        if int(iterations) > 0:
            for i in range(int(iterations)):
                # create new rankings dictionary
                new_rankings = update_rankings(mentions, rankings)
                rankings = new_rankings
    f.close()
    # create a pickle file of the final rankings
    with open(out_file, 'wb') as g:
        pickle.dump(rankings, g)


def words_dict(base_url: str, index_file: str, out_file: str) -> None:
    '''create a dictionary where the keys are all words in the web pages (in <p>s) and the values are dictionaries in which the keys are the links in index_file and the values are the number of times the word is mentioned in that link'''
    main_dict = {}
    with open(index_file, 'r') as links:
        for link in links:
            link = link.strip()
            soup = get_html_page_soup(base_url, link.strip())
            for p in soup.find_all('p'):
                # strip and turn into list of words
                content = p.text.strip().split()
                for word in content:
                    # for each word update the main_dictionary[word][link] with the count
                    if word in main_dict:
                        if link in main_dict[word]:
                            main_dict[word][link] += 1
                        else:
                            # if the link for the word isnt in the value dict add it
                            main_dict[word][link] = 1
                    else:
                        # if word isnt in main_dict add it and add link with value of 1
                        main_dict[word] = {}
                        main_dict[word][link] = 1
            # main_words_dict[link.strip()] = words_count
        links.close()
    # create a pickle file of the final rankings
    with open(out_file, 'wb') as g:
        pickle.dump(main_dict, g)


def pages_with_query(query: list, rankings: dict, words_dict: dict):
    '''returns pages that include querry word and have a ranking'''
    pages = [page for page in rankings]
    for word in query:
        # If word not in word_dict then skip because there aren't any links to compare
        if word not in words_dict:
            continue
        # Iterate over pages
        i = 0
        while i < (len(pages)):
            found = False
            # Check for each link if its in pages
            for link in words_dict[word]:
                if link == pages[i]:
                    found = True
            # If the pages isnt in word_dict[word]s' links then pop from list and adjust i
            if found == False:
                pages.pop(i)
                i -= 1
            i += 1
    return pages


def get_max_results(sorted_rankings, max_results, pages):
    '''returns top max_results relevant for search by rank descending'''
    # adjust max_ranks to sorted rankings length
    if max_results >= len(sorted_rankings):
        max_results = len(sorted_rankings) - 1
    results_dict = {}
    i = 0
    for link in sorted_rankings:
        # save only relevant pages
        if link in pages:
            results_dict[link] = sorted_rankings[link]
            i += 1
        if i > max_results - 1:
            break
    return results_dict
    ...


def calculate_overall_rank(sorted_rankings: dict, words_dict: dict, query):
    '''run algorithm to determine page ranking based on a query'''
    overall_rank = {link: 0 for link in sorted_rankings}
    # initialize a high number of mentions in case of multi worded query
    z_min = 10**8
    # for each webpage
    for link in sorted_rankings:
        # determine ranking based on word in query
        for word in query:
            if word in words_dict:
                if link in words_dict[word]:
                    # find minimum amount of mentions
                    if z_min > words_dict[word][link]:
                        z_min = words_dict[word][link]
                        min_word = word
        # calculate page ranking based on word with least mentions
        overall_rank[link] += words_dict[min_word][link] * \
            sorted_rankings[link]

    return overall_rank


def save_and_print_result(overall_rankings):
    '''appends results to results.txt and prints to screen'''
    with open("results.txt", "a") as f:
        for result in overall_rankings:
            val = result + " " + str(overall_rankings[result])
            f.write(val + "\n")
            print(val)
        f.write(10*"*" + "\n")


def search(query: str, ranking_dict_file: str, words_dict_file: str, max_results: int):
    '''Save a text file with the num(max_results) of links and rankings according to number of times mentiones and page ranking'''
    with open(words_dict_file, "rb") as f:
        words_dict = pickle.load(f)
        with open(ranking_dict_file, "rb") as g:
            rankings = pickle.load(g)
            # split query into list
            query: list = query.split(" ")
            # list of all pages with rankings
            pages = pages_with_query(query, rankings, words_dict)
            # sort rankings in descending order
            sorted_rankings = dict(sorted(rankings.items(),
                                          key=lambda item: item[1],
                                          reverse=True))
            # get max_result number of relevant pages sorted by rank
            results_dict = get_max_results(sorted_rankings, max_results, pages)
            # calculate overall ranking combining mentions in page and page rank
            overall_rankings = calculate_overall_rank(
                results_dict, words_dict, query)
            # double check results are sorted
            results = dict(sorted(overall_rankings.items(),
                                  key=lambda item: item[1],
                                  reverse=True))
            # save and print result in text file
            save_and_print_result(results)
            g.close()
        f.close()
    return


# run search engine from terminal
if __name__ == "__main__":
    func_to_run = sys.argv[1]
    if func_to_run == "crawl":
        #crawl(base_url, index_file, out_file)
        crawl(sys.argv[2], sys.argv[3], sys.argv[4])
    if func_to_run == "page_rank":
        page_rank(sys.argv[2], sys.argv[3], sys.argv[4])
    if func_to_run == "words_dict":
        words_dict(sys.argv[2], sys.argv[3], sys.argv[4])
    if func_to_run == "search":
        search(sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]))
