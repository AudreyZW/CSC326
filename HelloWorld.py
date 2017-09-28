from bottle import route, run
@route('/')
def hello():
	return "Hello World"
	
if __name__ == "__main__":

	try:
		run(host='localhost', port=8080, debug=True)
	except Exception,ex:
		print ex
