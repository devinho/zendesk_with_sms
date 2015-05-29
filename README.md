# SMS with Zendesk #

When we receive a text:
- search for a ticket for that phone number
- if an open ticket is found, append the text to the ticket
- if not, create a new ticket with the text

Replies to that ticket from an agent would be received by sms by the customer (no email)

How to configure Zendesk:

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
The targets will be triggered when certain actions are taken in Zendesk ex. Make an API call when a comment is made

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

You should be able to check this works by trying 'Test Target'

## 3. Create Triggers ##
We've created a target (send a text with twilio), now we need triggers

We will send a text when:
1. A comment has been made on your ticket
2. An agent has been assigned to your ticket
3. Your ticket has been marked as 'Solved'

To do this we need 4 triggers (one for when a ticket is commented on and marked 'Solved' at the same time)
The steps and specs are as follows:
- Go to settings (bottom-left gear)
- Go to 'Triggers'
- Click 'Add Trigger'
- Set fields as:
  ### Trigger 1 ###
  - Title: Notify requester of comment from agent (not solved)
  - Meet all of the following conditions:
    - Ticket: Is... / Updated
    - Ticket: Comment Is... / Present, and requester can see the comment
    - Other: Current user / Is / (agent)
    - Other: Current user / Is not / [admin that creates the tickets]
    - Ticket: Status / Is not / Solved
  - Perform these actions: 
    - Notifications: Notify Target / Twilio Notification (<- the target we just created!)
    - Message :
    - ```New comment from Agent {{ticket.latest_comment.author.name}} 
		{{ticket.latest_comment.created_at_with_time}}

		{{ticket.latest_comment}}

		Reply to this text to respond to this comment```


  ### Trigger 2 ###
  - test
