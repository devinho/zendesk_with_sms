# phone field id for zendesk = 25897847

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import urlparse
import json
import requests

ADDR = '45.55.212.169' #45.55.212.169
PORT = 8000

def createTicket(data):
    subject = 'SUBJECT'
    body = 'BODY'
    data = {'ticket': {'subject': subject, 'comment':{'body': body}, 'fields': {'25897847':'test'}}}

    payload = json.dumps(data)

    url = 'https://curbsidehelp.zendesk.com/api/v2/tickets.json'
    user = 'ho.devin05@gmail.com'
    pwd = '7ib18a8erhh'
    headers = {'content-type': 'application/json'}

    r = requests.post(url, data=payload, auth=(user,pwd), headers=headers)

    if r.status_code != 201:
        print('Status:', response.status_code, 'Problem with the request. Exiting.')    
        exit()

    print('Successfully created the ticket.')

class RequestHandler(BaseHTTPRequestHandler):        
    def do_GET(s):
        s.send_response(200)
        s.send_header('Content-type', 'text/html')
        s.end_headers()
        s.wfile.write('<body><p>Success</p></body>')

    def do_POST(s):
    	length = int(s.headers['Content-Length'])
    	post_data = urlparse.parse_qs(s.rfile.read(length).decode('utf-8'))



    	s.send_response(200)
        s.send_header('Content-type', 'text/html')
        s.end_headers()

        s.wfile.write('<body> <p>Success</p>')

        body = ''.join(post_data[u'Body'][0]).encode('ascii', 'ignore')
        phone = ''.join(post_data['From'][0]).encode('ascii', 'ignore')

        position = body.find(' ')

        if position == -1:
            command = body
            remainder = ''
        else:
            command = body[0:position]
            remainder = body[position:len(value)]

        if command == 'menu':
            print '\nThe available commands are:\r\n'
            print 'new - create a new ticket\r'
            print '[id] - update this ticket ID\r'
            print 'menu - show this menu\r\n'
        elif command == 'new':
            #createTicket(remainder)
            print phone
        elif command.isdigit():
            print 'isdigit'
        else:
            print '\nHello and thanks for the message.\r'
            print 'Unfortunately I did not quite understand what you needed.\r'
            print 'Try sending the word "menu" for the list of commands.\r\n'
        # s.wfile.write('<p>%s=%s</p>'  % (key, value))
        # print '%s=%s , ' % (key, value)


        s.wfile.write('</body>')


httpd = HTTPServer((ADDR, PORT), RequestHandler)
httpd.serve_forever()