from bottle import route, run

@route('/')

def home():
    return '<html><body>This is what links to the first page.</body></html>'

run(host='0.0.0.0', port=8090, debug=True)

