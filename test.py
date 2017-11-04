
'''This test creates one page hosted by bottle on port 8090 which contains some text and then
links to another page which also has text. We expect the crawler to crawl through the first page
and then to go into the embedded link as well.'''

from bottle import route, run, redirect

@route('/')

#host the main page and create a link to the linker page
def home():
    return '<html><body>This is a very simple test.<a href= "http://localhost:8090/link">Linker page</a></body></html>'

#redirect to the linker page
@route('/link')
def link():
    redirect('/linker')

#the linker page
@route('/linker')
def linker():
    return '<html><body>This is what links to the first page.<a href= "http://localhost:8090/finallink">Final Link page</a></body></html>'


@route('/finallink')
def final_link():
    redirect('/finallinkpage')

@route('/finallinkpage')
def final_linkpage():
    return '<html><body>This is our final page. <a href = "http://localhost:8090/something">Back</a></body></html>'

@route('/something')
def something():
    redirect('/linker')



run(host='localhost', port=8090, debug=True)