from bottle import route, run, redirect

@route('/')

def home():
    #redirect("http://localhost:8090/")
    return '<html><body>This is a very simple test.<a href= "http://localhost:8080/link">Linker page</a></body></html>'

@route('/link')
def link():
    redirect('/linker')

@route('/linker')
def linker():
    return '<html><body>This is what links to the first page.</body></html>'


run(host='localhost', port=8080, debug=True)


