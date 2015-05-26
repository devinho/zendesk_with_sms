# phone field id for zendesk = 25897847

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import urlparse
import json
import requests
from twilio.rest import TwilioRestClient 

ADDR = '45.55.212.169' #45.55.212.169
PORT = 8000

def sendText(phone, message):
    ACCOUNT_SID = "AC259e229cc7f22e3922ba82ae2fff1232" 
    AUTH_TOKEN = "58c17f647492900c6a9701739387ee5c" 

    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 
    client.messages.create(
        to = phone, 
        from_ = '+16504698204',   
        body = message,
    )

def createTicket(subject, phone):
    subject = subject
    body = subject
    data = {'ticket': {'subject': subject, 'comment':{'body': body}, 'fields': {'25897847': phone}}}

    payload = json.dumps(data)

    url = 'https://curbsidehelp.zendesk.com/api/v2/tickets.json'
    user = 'ho.devin05@gmail.com'
    pwd = '7ib18a8erhh'
    headers = {'content-type': 'application/json'}

    r = requests.post(url, data=payload, auth=(user,pwd), headers=headers)

    if r.status_code != 201:
        print('Status:', r.status_code, 'Problem with the request.') 
        sendText(phone, 'Something went wrong. Your ticket was not created.')
    else:
        iD = r.json()['ticket']['id']
        print('Successfully created the ticket.')
        sendText(phone, 'A new ticket has been created. To add a comment, reply with command: "' + str(ticket) + ' [message]"');
        return iD

def updateTicket(ticket, comment, phone):
    url = 'https://curbsidehelp.zendesk.com/api/v2/tickets/' + str(ticket) + '.json'
    user = 'ho.devin05@gmail.com'
    pwd = '7ib18a8erhh'
    headers = {'content-type': 'application/json'}
    r = requests.get(url, auth=(user,pwd))
    
    if r.status_code != 200:
        print ('Ticket not found')
    else:
        data = {'ticket': {'comment': {'body': comment}}}
        payload = json.dumps(data)
        r2 = requests.put(url, data=payload, headers=headers, auth=(user,pwd))
        if r2.status_code != 200:
            print('Status:', response.status_code, 'Problem with the request.')
            sendText(phone, 'We could not find your ticket with ID '+ str(ticket) +'. Are you sure that\'s the right ID?')
        else:
            print('Successfully added comment to ticket')
            sendText(phone, 'Your ticket('+ str(ticket) +') has been updated. We\'ll get to it as soon as we can.')

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

        body = ''.join(post_data['Body'][0]).encode('ascii', 'ignore')
        phone = ''.join(post_data['From'][0]).encode('ascii', 'ignore')

        position = body.find(' ')

        if position == -1:
            command = body
            remainder = ''
        else:
            command = body[0:position]
            remainder = body[position+1:len(body)]

        if command == 'menu':
            message = '\nThe available commands are:\nnew - create a new ticket\n[id] - update this ticket ID\nmenu - show this menu\n'
            print message
            # print '\nThe available commands are:\n'
            # print 'new - create a new ticket'
            # print '[id] - update this ticket ID'
            # print 'menu - show this menu\n'
        elif command == 'new':
            ticket = createTicket(remainder, phone)
        elif command.isdigit():
            updateTicket(command, remainder, phone)
        else:
            print '\nHello and thanks for the message.'
            print 'Unfortunately I did not quite understand what you needed.'
            print 'Try sending the word "menu" for the list of commands.\n'
        # s.wfile.write('<p>%s=%s</p>'  % (key, value))
        # print '%s=%s , ' % (key, value)


        s.wfile.write('</body>')


httpd = HTTPServer((ADDR, PORT), RequestHandler)
httpd.serve_forever()