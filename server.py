# phone field id for zendesk = 25897847

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import urlparse

ADDR = "localhost"
PORT = 8000

class RequestHandler(BaseHTTPRequestHandler):        
    def do_GET(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<body><p>This is a test.</p>")

    def do_POST(s):
    	length = int(s.headers['Content-Length'])
    	post_data = urlparse.parse_qs(s.rfile.read(length).decode('utf-8'))



    	s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

        s.wfile.write("<body>")
        for key, value in post_data.iteritems():
    		s.wfile.write("<p>%s=%s</p>"  % (key, value))

        s.wfile.write("</body>")

       

    	


httpd = HTTPServer((ADDR, PORT), RequestHandler)
httpd.serve_forever()