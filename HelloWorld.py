import re # python regular expressions for stripping out symbols
from collections import Counter # used to count occurrences of words
import httplib2 # a HTTP client library; we apply credentials to an httplib2.Http() object, so future HTTP requests will be authorized those credentials
from beaker.middleware import SessionMiddleware # Beaker's session management library (session keeps data for you, just like cookies)

import bottle
from bottle import route, get, post, request, response, run, template, static_file

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

# Configure the SessionMiddleware
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}
app = SessionMiddleware(bottle.app(), session_opts) # app is now a replacement of original bottle.app(); if not specified in run() at bottom, default app will be run
user_words= {} # users' search history; a dict of dict: <user_email,<word,count>>
user_recent= {} # 10 recently searched words of a user from earlist to lastest; a dict of list: <user_email,[words]>

# Our application asks Google for access to user info
@route('/google_auth', 'GET')
def google_auth():
    # create a Flow from a clientsecrets file
    flow = flow_from_clientsecrets("client_secret.json", 
            scope='https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile', # https://www.googleapis.com/auth/plus.me
            redirect_uri="http://localhost:8080/redirect")
    # generate the Google authorization server URI
    uri = flow.step1_get_authorize_url()
    bottle.redirect(str(uri))

# If user authorizes our application by logging in to their Google account, an onetime authorization code will be attached
# to the query string when the browser is redirected to '/redirect'. The onetime code can be retrieved as GET parameter,
# then used to exchange for an access token
@route('/redirect', 'GET')
def redirect_page():
    code = request.query.get('code', '') # if code is not granted to us, return empty string
    # create a Flow again to get credentials
    flow = OAuth2WebServerFlow(client_id= "85110286458-6jnah4v02br46rbe6v433pt0a22jtgin.apps.googleusercontent.com", 
            client_secret= "RMeHRVe8dbjikduKTlU4b5EO",
            scope= "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile", # https://www.googleapis.com/auth/plus.me
            redirect_uri= "http://localhost:8080/redirect")
    # exchanges an authorization code for a Credentials object, which holds refresh and access tokens for access to user data
    credentials = flow.step2_exchange(code)

    # apply credentials to an httplib2.Http() object, so any HTTP requests made with this object will be authorized those credentials
    http = httplib2.Http()
    http = credentials.authorize(http)
    
    session = request.environ.get('beaker.session')
    # Get user email, user name and profile pic if they exist
    users_service = build('oauth2', 'v2', http=http) # build(serviceName, version, http=None)
    user_document = users_service.userinfo().get().execute()
    session['email'] = user_document['email']
    if 'name' in user_document: session['name'] = user_document['name']
    if 'picture' in user_document: session['picture'] = user_document['picture']
    
    if False:""" Google Plus api
    plus_service = build('plus', 'v1', http=http)
    people_resource = plus_service.people()
    people_document = people_resource.get(userId='me').execute()
    print "Display name: " + people_document['displayName']
    print "Image URL: " + people_document['image']['url']
    """
    session['name'] = user_document['name']
    
    # retrieved all user data we need, now redirect to the page where the user comes from
    bottle.redirect('/')
    
@route('/logout', 'GET')
def logout():
    session = request.environ.get('beaker.session')
    session.delete()
    # in case user has logged in but user history has been lost when server gets reloaded
    if 'email' in session and session['email'] and session['email'] in user_words:
        # when a user logs out, only leave the 20 most searched words in its history and delete the rest
        keywords_countdown= sorted(user_words[session['email']].items(), key= lambda word: word[1], reverse=True)
        if len(keywords_countdown)> 20:
            for word,count in keywords_countdown[20:]: 
                del user_words[user_email][word]
            
    session.delete()
    bottle.redirect('/')

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
        session = bottle.request.environ.get('beaker.session')
        user_email= session.setdefault('email', '') # set email to empty string if user not logged in
        recent_list= []
        keywords_countdown= []
        
        if user_email: # if user is logged in
            if not user_words.has_key(user_email): # if no past records for this user
                user_words[user_email]= {} # initialize the dict for this user to store keywords searched--<key:word, value:count> in cookies
                user_recent[user_email]= [] # initialize the list for this user to store 10 most recent words
                
        input_words = re.sub(r'([^\s\w])+', "", input_words) # strip everything other than alphanumeric (which includes '_') and spaces
        input_lower= input_words.lower() # convert input_words to lowercase
        word_list = input_lower.split()
        word_counter = Counter(word_list) # an unordered dictionary--<key:word, value:count>
        # if user is logged in, record words and count
        if user_email:
            for word,count in word_counter.items():
                # if this word has been searched before, add up its count; else, record its count
                user_words[user_email][word]= user_words[user_email].get(word, 0)+ count
            # display most searched words for the user
            keywords_countdown= sorted(user_words[user_email].items(), key= lambda word: word[1], reverse=True)
            
        word_list_clean = rm_duplicates(word_list) # remove duplicate words while maintaining original order
        # if user is logged in, update 10 most recent words
        if user_email:
            for word in word_list_clean:
                if word in user_recent[user_email]: user_recent[user_email].remove(word)
            l= word_list_clean+ user_recent[user_email]
            user_recent[user_email]= l[:10] # only take the 10 most recent words
            recent_list= l[:10]
        
        return template('resultpage', input_words= input_words, word_list_clean= word_list_clean, word_counter= word_counter, 
                        user_email= user_email, session= session, recent_list= recent_list, keywords_countdown= keywords_countdown)

@get('/')
def root_path():
    # if user hasn't submitted any input or has just completed a search
    if not request.query.get('keywords', ''):
        session = bottle.request.environ.get('beaker.session') # Get the session object from the environ
        user_email= session.setdefault('email', '') # set email to empty string if user not logged in
        keywords_countdown= [] # initialize countdown list
        
        # if user is logged in and there are records of past searches for this user
        if user_email and user_words.has_key(user_email):
            # a list of tuples (word, count_total) of searched words, sorted in descending order of count_total
            # (this sorting by value does not affect the dict itself)
            # lambda: take each pair in dict as word and use word[1] as comparison key for sorting (word[0] is key, word[1] is value)
            keywords_countdown= sorted(user_words[user_email].items(), key= lambda word: word[1], reverse=True)
            
        return template('homepage', keywords_countdown= keywords_countdown, user_email= user_email, session= session)
    # display result page with word counts
    else:
        return parse_input()

if __name__=="__main__":
    run(app=app, host='localhost', port=8080, debug=True, reloader=True) # host='128.100.13.175'
