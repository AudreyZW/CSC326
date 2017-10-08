from bottle import route, run

@route('/')

def home():
    return '<html><body>This is a very simple test case for CSC326.<a href = "http://192.168.1.10:8090/" My link </a> </body></html>'

run(host='0.0.0.0', port=8080, debug=True)

