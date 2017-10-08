import re # python regular expressions for stripping out symbols
from collections import Counter # used to count occurrences of words

from bottle import route, get, post, request, response, run, template, static_file

if False: """
def word_count(list):
    word_counter = dict()
    for i in list:
        word_counter[i] = word_counter.get(i,0) +1 # return 0 if key i doesn't exist in the dictionary yet
    return word_counter
"""

def rm_duplicates(list): # remove duplicates
    seen = set()
    new_list = [] # a new list without duplicates but with original order
    for elem in list:
        if elem not in seen:
            seen.add(elem)
            new_list.append(elem)
    return new_list

@route('/<filename:re:.*\.png>')
def send_image(filename):
    return static_file(filename, root='') # root= relative path to the folder that contains the file, the png file is in the same folder as this py file, hence path is empty

#@get('/parse') # or @route('/', method='POST')
def parse_input():
    input_words = request.query.get('keywords')
    request.query.replace('keywords', '') # clear 'keywords' to display query page again after this search
    
    if len(input_words)<= 0:
        return "<p>Input is empty.</p>"
    else:
        input_words = re.sub(r'([^\s\w])+', "", input_words) # strip everything other than alphanumeric (which includes '_') and spaces
        input_lower= input_words.lower() # convert input_words to lowercase
        word_list = input_lower.split()
        word_counter = Counter(word_list) # an unordered dictionary--<key:word, value:count>
        for word,count in word_counter.items():
            if request.get_cookie(word): # if this word has been searched before, add up its count
                count_total= int(request.get_cookie(word)) + count
                response.set_cookie(word, str(count_total))
            else: # if this word has never been searched before, record its count in cookies
                response.set_cookie(word, str(count))
        
        word_list_clean = rm_duplicates(word_list) # remove duplicate words while maintaining original order
        print "word_list_clean: "
        print word_list_clean
        
        return template(''' 
            <style> 
                td, th {border: 1px solid #dddddd; text-align: left} 
            </style>
            <p>Searched for "{{input_words}}"</p>
            <table id="results">
                <col width="130">
                <tr>
                  <th>Word</th> <th>Count</th>
                </tr>
                % for word in word_list_clean: # display words in original order
                    <tr>
                      <td>{{word}}</td> <td>{{word_counter[word]}}</td>
                    </tr>
                % end
            </table> 
        ''', input_words= input_words, word_list_clean= word_list_clean, word_counter= word_counter)

@get('/')
def root_path():
    if not request.query.get('keywords', ''): # if user hasn't submitted any input or has just completed a search
        keywords_countdown= [('','')] # initialize countdown list
        if request.cookies:
            # a list of tuples (word, count_total) of searched words, sorted in descending order of count_total
            keywords_countdown= sorted(request.cookies.items(), key= lambda word: int(word[1]), reverse=True)
            if False: """for word in request.cookies:
                print "cookie: "+word
                print request.get_cookie(word)
                """
        if False: """input[type="text"] {
                display: block;
                margin : 0 auto;
            }"""
        
        return template('''
            <style>
            img {
                display: block;
                margin: 100 auto;
            }
            </style>
            <img src="logo.png" alt="website logo" height="100">
            <form action="/" method="get">
                Input: <input name="keywords" type="text" />
                <input value="Submit" type="submit" />
            </form>
            <br>
            <p>Search history:</p>
            <table id="history">
                <col width="130">
                <tr>
                  <th>Word</th> <th>Count</th>
                </tr>
                % for word,count in keywords_countdown[:20]: 
                    <tr>
                      <td>{{word}}</td> <td>{{count}}</td>
                    </tr>
                % end
                </table>
        ''', keywords_countdown= keywords_countdown)
    else: # display result page with word counts
        return parse_input()

if __name__=="__main__":
    run(host='localhost', port=8080, debug=True, reloader=True) # host='127.0.0.1'
