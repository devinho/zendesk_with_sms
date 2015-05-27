from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import urlparse
import json
import requests
from twilio.rest import TwilioRestClient 
import os

ADDR = 'localhost' #45.55.212.169
PORT = 8000

# zendesk login credentials
user = os.getenv('email')
pwd = os.getenv('pass')
zendesk_url = 'https://curbsidehelp.zendesk.com'
phone_field_id = 25897847  # field id for custom field in zen desk

def send_text(phone, message):

    # twilio authentication 

    ACCOUNT_SID = "AC259e229cc7f22e3922ba82ae2fff1232" 
    AUTH_TOKEN = "58c17f647492900c6a9701739387ee5c" 
    twilio_phone = '+16504698204'

    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 
    # send text message
    client.messages.create(
        to = phone, 
        from_ = twilio_phone,
        body = message,
    )

# create a zendesk ticket (called when text message is sent from a phone number that doesn't have an existing ticket) 
# subject = body of ticket
# phone = phone number that sent text message

def create_ticket(subject, phone):
    subject = subject
    body = subject
    data = {'ticket': {'subject': subject, 'comment':{'body': body}, 'fields': {phone_field_id: phone}}}

    payload = json.dumps(data)

    url = zendesk_url + '/api/v2/tickets.json'

    headers = {'content-type': 'application/json'}
    
    r = requests.post(url, data=payload, auth=(user,pwd), headers=headers)

    # if for some reason posting new ticket to zendesk does not work

    if r.status_code != 201:
        print('Status:', r.status_code, 'Problem with the request.') 
        send_text(phone, 'Something went wrong. Your ticket was not created.')
    else:
        ticket_id = r.json()['ticket']['id']
        print('Successfully created the ticket.')
        send_text(phone, 'A new ticket has been created (id = ' + str(iD) + '). To add a comment, just send another text message.');
        return ticket_id

# update an existing zendesk ticket (text message is received from a number that already has an existing ticket open)
# ticket = ticket id
# comment = text of comment
# phone = phone number that the ticket belongs to

def update_ticket(ticket, comment, phone):
    url = zendesk_url + '/api/v2/tickets/' + str(ticket) + '.json'

    headers = {'content-type': 'application/json'}
    r = requests.get(url, auth=(user,pwd))
    
    if r.status_code != 200:
        print ('Ticket not found')
        send_text(phone, 'We could not find your ticket.') # This should never happen (ticket is created if ticket not found)
    else:
        data = {'ticket': {'comment': {'body': comment}}}
        payload = json.dumps(data)
        r2 = requests.put(url, data=payload, headers=headers, auth=(user,pwd))
        if r2.status_code != 200:
            print('Status:', response.status_code, 'Problem with the request.')
            send_text(phone, 'We could not add your comment to ticket ('+ str(ticket) +').')
        else:
            print('Successfully added comment to ticket')
            send_text(phone, 'Your ticket ('+ str(ticket) +') has been updated. We\'ll get to it as soon as we can.')

# return ticket id for given phone number. if it doesn't exist return -1
# phone = phone number to search a ticket for

def find_ticket(phone):
    ticket_id = -1
    url = zendesk_url + '/api/v2/tickets.json'
    headers = {'Accept':'application/json'}
    r = requests.get(url, auth=(user,pwd), headers=headers)
    for ticket in r.json()['tickets']:
        if ticket['status'] != 'solved' and ticket['custom_fields'][0]['value'] == phone:
            ticket_id = ticket['id']

    return ticket_id


class RequestHandler(BaseHTTPRequestHandler):   
    def do_GET(s):
        #work around for sending text when comment is posted to existing ticket
        q = urlparse.parse_qs(urlparse.urlparse(s.path).query)

        send_text(q['to'][0],'\n' + q['Body'][0] + '\n')

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


        # 'Body' and 'From' are required to create/update a ticket
        body = ''.join(post_data['Body'][0]).encode('ascii', 'ignore')
        phone = ''.join(post_data['From'][0]).encode('ascii', 'ignore')

    
        ticket_id = find_ticket(phone)

        if ticket_id != -1:
            # if ticket already exists, append text to ticket
            update_ticket(ticket_id, body, phone)
        else:
            # if ticket does not exist, create a new ticket
            create_ticket(body, phone)


        # OLD MENU SYSTEM

        # position = body.find(' ')

        # if position == -1:
        #     command = body
        #     remainder = ''
        # else:
        #     command = body[0:position]
        #     remainder = body[position+1:len(body)]

        # if command == 'menu':
        #     message = '\nThe available commands are:\nnew - create a new ticket\n[id] - update this ticket ID\nmenu - show this menu\n'
        #     send_text(phone, message)
        # elif command == 'new':
        #     ticket = create_ticket(remainder, phone)
        # elif command.isdigit():
        #     update_ticket(command, remainder, phone)
        # else:
        #     message = 'Hello and thanks for the message. Unfortunately I did not quite understand what you needed. Try sending the word "menu" for the list of commands.\n'
        #     send_text(phone, message)


        # s.wfile.write('<p>%s=%s</p>'  % (key, value))
        # print '%s=%s , ' % (key, value)

        s.wfile.write('</body>')

httpd = HTTPServer((ADDR, PORT), RequestHandler)
httpd.serve_forever()
