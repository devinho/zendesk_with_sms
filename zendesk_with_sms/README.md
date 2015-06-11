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

Leave everything as is. We will finish this once we deploy our app.

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
  - URL: (set a placeholder url for now. we will add later)
  - Method: Get
  - Attribute Name: body
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
Note: Used Python 2.7.9

```
git clone https://github.com/devinho/curbside.git
```

## 1. Set up Google App Engine

To download App Engine, follow instructions at:

https://cloud.google.com/appengine/docs/python/gettingstartedpython27/introduction

Once downloaded, open App Engine and add zendesk_with_sms as an existing application by doing:
File -> Add Existing Application -> browse -> path/to/curbside/zendesk_with_sms -> add


```
cd curbside
cd zendesk_with_sms
pip install -t lib -r requirements.txt
```


## 2. Create config.py:
```
# Twilio 
ACCOUNT_SID = '[your account_sid]'
AUTH_TOKEN = '[your auth_token]'
twilio_phone = '[your twilio phone number]'

# Zendesk 
user = '[your zendesk username]'
pwd = '[your zendesk password]'
zendesk_url = '[your zendesk domain]'
phone_field_id  = '[your custom field id]'
```

## 3. Run app

```
cd ..
dev_appserver.py zendesk_with_sms/
```
(Need to be in parent ../curbside not ../curbside/zendesk_with_sms) 

## 4. Deployment to App Engine and Final Twilio/Zendesk config

Follow instructions at:

https://cloud.google.com/appengine/docs/python/gettingstartedpython27/uploading

Once your app is deployed, make sure it works at:

http://your-app-id.appspot.com/

### Final Twilio Config

Now we need to configure Twilio and Zendesk so it points at this URL.

For Twilio head to the number you created and set the Request URL for SMS & MMS to your app engine URL.


### Final Zenesk Config

Head to Zendesk Target we created. Now instead of the placeholder from before, put:

http://your-app-id.appspot.com/?to={{ticket.ticket_field_[YOUR_PHONE_TICKET_FIELD]}}



Misc notes:

- In Zendesk, the tickets will be created under the user the login credentials are for. This user only be used for creating tickets and assigning them. Only agents assigned to tickets should comment on them.
- If you are using a trial Twilio account, you can only send texts to approved numbers.



