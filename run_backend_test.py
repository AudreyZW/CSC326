import pprint
import crawler
import operator
from collections import OrderedDict

if __name__ == "__main__":
    bot = crawler.crawler(None, "urls.txt")
    bot.crawl(depth=1)

    inverted_index = bot.get_inverted_index()
    resolved_inverted_index = bot.get_resolved_inverted_index()
    document_index = bot._url_list

    #print bot.get_inverted_index()
    #print bot.get_resolved_inverted_index()
    #stuff = ['Doc ID', 'PageRank Scores']
    #stuff.insert(0, stuff[:])
    #pp =pprint.PrettyPrinter(indent=2)


    #score_list is dictionary
    score_list = bot.get_docid_score()

    #score_list_descending is the sorted dictionary
    #score_list_descending = OrderedDict(sorted(score_list.items(), reverse = True))


    sorted_score = sorted(score_list.items(), key=operator.itemgetter(1), reverse = True)

    pprint.pprint(sorted_score, width=1)

    bot.initialize_tables()
    bot.store_to_database()