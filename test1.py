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
    return '<html><body>This is what links to the first page.</body></html>'


run(host='localhost', port=8090, debug=True)


