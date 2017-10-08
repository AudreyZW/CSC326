from bottle import route, run

@route('/linker')

def linker():
    return '<html><body>This is what links to the first page.</body></html>'

run(host='localhost', port=8080, debug=True)

