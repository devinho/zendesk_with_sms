import os

# twilio

ACCOUNT_SID = "AC054da9e69b02dc42dc306cd9ce60a7f9" 
AUTH_TOKEN = "a87a3720a186d2fdfdf7f9074fec7344" 
twilio_phone = '+14089139034'

# zendesk
user = os.getenv('email')
pwd = os.getenv('pass')
zendesk_url = 'https://curbsidehelp.zendesk.com'
phone_field_id = 25897847  # field id for custom field in zen desk
