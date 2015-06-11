# Zendesk with SMS

When we receive a text:
- search for a ticket for that phone number
- if an open ticket is found, append the text to the ticket
- if not, create a new ticket with the text

Replies to that ticket from an agent would be received by sms by the customer (no email)

Opening a ticket and leaving comments to a ticket will look like a regular conversation with a user

To do this we will use Zendesk and Twilio

# How to configure Twilio

Create a new twilio number

For the new number, set the request URL to the IP the python server will run on

# How to configure Zendesk

## 1. Create phone field ##
This field will hold customer's phone number

- Go to settings (bottom-left gear)
- Go to 'Ticket Fields'
- Click 'Add Custom Field'
- Select 'Text'
- Set 'Field Title' to 'Phone'
- Press 'Add Field'

The last thing that needs to be done is to get the field id for our custome field
- From the 'Ticket Fields' list, edit the 'Phone' we just created
- Note the 'Custom Field id' and save for future reference


## 2. Create Targets ##
The targets will be triggered when certain actions are taken in Zendesk (ex. make an API call when a comment is made)

- Go to settings (bottom-left gear)
- Go to 'Extensions'
- Click 'Add Target'
- Select 'URL Target'
- Set fields as:
  - Title: Twilio Notification
  - URL: [IP FOR SERVER]
  - Method: Get
  - Attribute Name: Body
  - No basic authentication

You should be able to check this works by trying 'Test Target' (python server needs to be running)

## 3. Create Triggers ##
We've created a target (send a text with twilio), now we need a trigger 

This trigger will get called everytime a comment is made on a ticket 

The steps and specs are as follows:
- Go to settings (bottom-left gear)
- Go to 'Triggers'
- Click 'Add Trigger'
- Set fields as follows:

### Trigger 1 
  A comment has been made on your ticket
  - Title: Notify requester of all comments

    - Ticket: Comment Is... / Public
    - Other: Current user / Is / (agent)

  - Perform these actions: 
    - Notifications: Notify Target / Twilio Notification <- the target we just created!
    - Message :
	   >{{ticket.latest_comment}}

# How to set up python server

```git clone https://github.com/devinho/curbside.git```
```cd zendesk_with_sms```
```pip install -t lib -r requirements.txt```


## Set up config.py
Create config.py and add the following:
- Twilio ACCOUNT_SID, AUTH_TOKEN, and phone number
- Zendesk username, password, domain, and custom phone field (ID marked down earlier)

## Set up Google App Engine

Follow instructions at:

https://cloud.google.com/appengine/docs/python/gettingstartedpython27/introduction



``` python server.py ```

Misc notes:

- In Zendesk, the tickets will be created under the user the login credentials are for. This user only be used for creating tickets and assigning them. Only agents assigned to tickets should comment on them.
- If you are using a trial Twilio account, you can only send texts to approved numbers.



