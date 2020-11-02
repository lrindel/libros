import http.server
import json
import urllib.request
import re

libros = [
	{
		"id":0,
		"titulo":"libro cero",
		"autorid":0
	},
	{
		"id":1,
		"titulo":"libro uno",
		"autorid":0
	},
	{
		"id":2,
		"titulo":"libro dos",
		"autorid":1
	}
]

def httpGET(URL, DATA):
	result = None
	
	request = urllib.request.Request(
		url = URL,
		data = DATA)

	response = None
	try:
		response = urllib.request.urlopen(request)
		
		# valido
		print(response.status)
		print(response.reason)
		result = response.read().decode()
		
	except Exception as e:
		print ("ERROR")
		print (e)
		raise(e)
		
	return result


class LibrosHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
	def do_GET(self): 
		response = ""
		
		print(self.path)
		
		if (self.path == "/libros/"):
			response = json.dumps(libros, indent=2)
			
		else:
			m = re.search("/libro/([0-9]+)/", self.path)
			if (m):
				print(m.group(1))
				libro = [l for l in libros if l["id"] == int(m.group(1))][0]
				libro["autor"] = json.loads(httpGET("http://localhost:8081/autor/" + str(libro["autorid"]) + "/", None))
				response = json.dumps(libro, indent=2)
			
		self.wfile.write(b"HTTP/1.1 200 OK\n")
		self.wfile.write(b"\n")
		self.wfile.write(response.encode())

httpd = http.server.HTTPServer(("",8080), LibrosHTTPRequestHandler)
httpd.serve_forever()