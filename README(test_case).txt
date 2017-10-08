Our test has the main page running at port localhost:8090. 
This page has 6 words as seen by the result of the crawler ( omitting the ignored words)
The lexicon is [This, very, simple, test, Linker, page]
The inverted index maps these words to the url "http://localhost:8090"
as can be seen by the results.

This page has a link which leads to the url 'http://localhost:8090/link'
which contains 6 words as well. 
The lexicon is [This, what, links, to, first, page]


This is the output:

From this we can take the example of the word "page" which has the word_id 6. This corresponds to the set[1,2] which corresponds to the both the urls http://localhost:8090/link and http://localhost:8090.
This means that the word is contained in both pages which is correct since we can see that in our lexicons and directly on the webpages if we compare them. Therefore, our test is successful.

Inverted_index: {1: set([1, 2]), 2: set([1]), 3: set([1]), 4: set([1]), 5: set([1]), 6: set([1, 2]), 7: set([2]), 8: set([2]), 9: set([2]), 10: set([2])}


Resolved_index: {u'what': set([u'http://localhost:8090/link']), u'links': set([u'http://localhost:8090/link']), u'to': set([u'http://localhost:8090/link']), u'this': set(['http://localhost:8090/', u'http://localhost:8090/link']), u'linker': set(['http://localhost:8090/']), u'very': set(['http://localhost:8090/']), u'test': set(['http://localhost:8090/']), u'page': set(['http://localhost:8090/', u'http://localhost:8090/link']), u'simple': set(['http://localhost:8090/']), u'first': set([u'http://localhost:8090/link'])}


Id- to - url dictionary: {1: 'http://localhost:8090/', 2: u'http://localhost:8090/link'}


Id- to - word dictionary: {1: u'this', 2: u'very', 3: u'simple', 4: u'test', 5: u'linker', 6: u'page', 7: u'what', 8: u'links', 9: u'to', 10: u'first'}
