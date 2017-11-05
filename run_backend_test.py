import pprint
import crawler
import operator
import string
from collections import OrderedDict

'''In order to run this code, simply run the file pagerank.py'''

'''This file imports the crawler to crawl through the document and stores the scores of the pages into a list. We then 
sort that list in descending order and then print out the document ids and their scores.'''

if __name__ == "__main__":

    #creating an instance of the crawler
    bot = crawler.crawler(None, "urls.txt")
    bot.crawl(depth=1)

    #score_list is dictionary which maps the score of the document to its docid
    score_list = bot.get_docid_score()

    #sort the scores in descending order
    sorted_score = sorted(score_list.items(), key=operator.itemgetter(1), reverse = True)

    #pretty print the sorted scores and the document ids
    for i in sorted_score:
        pprint.pprint(list(i))
