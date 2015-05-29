# twilio
ACCOUNT_SID = "asdf" 
AUTH_TOKEN = "asdf" 
twilio_phone = '+123'

# zendesk
user = 'email'
pwd = 'password'
zendesk_url = 'https://domain.zendesk.com'
phone_field_id = 1234567  # field id for custom field in zen desk


try:
	from config import *
except Exception as inst:
	print inst