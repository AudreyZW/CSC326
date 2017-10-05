import re # python regular expressions for stripping out symbols
from collections import Counter # used to count occurrences of words

from bottle import route, get, post, request, run, template, static_file

if False: """
def word_count(list):
    word_counter = dict()
    for i in list:
        word_counter[i] = word_counter.get(i,0) +1 # return 0 if key i doesn't exist in the dictionary yet
    return word_counter
"""

def rm_duplicates(list): # remove duplicates
    seen = set()
    for i, elem in enumerate(list):
        if elem not in seen:
            seen.add(elem)
        else:
            del list[i]
    return list

@route('/<filename:re:.*\.png>')
def send_image(filename):
    return static_file(filename, root='') # root= relative path to the folder that contains the file, the png file is in the same folder as this py file, hence path is empty

@get('/')
def ask_input():
    return '''
        <img src="logo.png" alt="website logo" height="50">
        <form action="/parse" method="get">
            Input: <input name="input" type="text" />
            <input value="Submit" type="submit" />
        </form>
    '''
    
@get('/parse') # or @route('/', method='POST')
def parse_input():
    input = request.query.get('input')
    if len(input)<= 0:
        return "<p>Input is empty.</p>"
    else:
        input = re.sub(r'([^\s\w])+', "", input) # strip everything other than alphanumeric (which includes '_') and spaces
        input_lower= input.lower() # convert input to lowercase
        word_list = input_lower.split()
        word_counter = Counter(word_list) # an unordered dictionary--<key:word, value:count>
        word_list_clean = rm_duplicates(word_list) # remove duplicate words while maintaining original order
        
        return template(''' 
            <style> 
                td, th {border: 1px solid #dddddd; text-align: left} 
            </style>
            <p>Searched for "{{input}}"</p>
            <table>
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
        ''', input= input, word_list_clean= word_list_clean, word_counter= word_counter)

if __name__=="__main__":
    run(host='localhost', port=8080, debug=True, reloader=True) # host='127.0.0.1'
