from bottle import route, run,redirect

@route('/')

def home():
    redirect("http://localhost:8080/linker")
run(host='localhost', port=8080, debug=True)

