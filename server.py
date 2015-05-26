# phone field id for zendesk = 25897847

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import urlparse

ADDR = "localhost" #45.55.212.169
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
        	if key == "Body":
        		body = ''.join(value).encode('ascii', 'ignore')

        		position = body.find(" ")

        		if position == -1:
        			command = body
        		else:
        			command = body[0:position]
        			remainder = body[position:len(value)]

        		if command == "menu":
        			print "The available commands are:\r\new - create a new ticket\r\n"
        			print "[id] - update this ticket ID\r\n"
        			print "menu - show this menu"
        		elif command == "new":
        			print "new"
        		elif command.isdigit():
        			print "isdigit"
        		else:
        			print "Hello and thanks for the message. Unfortunately I did not quite understand what you needed."
    			#s.wfile.write("<p>%s=%s</p>"  % (key, value))
    			#print "%s=%s , " % (key, value)
        s.wfile.write("</body>")

       

    	


httpd = HTTPServer((ADDR, PORT), RequestHandler)
httpd.serve_forever()