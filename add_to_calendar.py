import json, textwrap, datetime, subprocess
import email, email.policy
import openai
from googleapiclient.discovery import build
from google.oauth2 import service_account

instructions = \
"""You are AI assistant helping users to process their incoming emails and maintain their calendar.
In this specific instance, your task is to generate calendar event descriptions from emails. The 
user will send you the text of an email they have received and that contains information on an 
event that they wish to offer to their calender. You should reply with a JSON object that is 
suitable for upload with Google's API. 

Make sure your answer is a bare JSON object, without surrounding punctuation like backticks --
so that you reply can be directly passed to a JSOM parser.

When writing the description, please rephrase and summarize the mail suitably to three or four 
sentences. Remove redundant information that is available in other fields of the JSON structure.
For the summary, include a, possibly shortened, title or the topic in case of seminars.

Unless the mail specifies otherwise, assume Europe/Berlin time.

The JSON event object must not include an invitation of attendees.

Add the end of the summary, add a line like "created from e-mail mid:<message-id>", replacing
<message-id> with the specified message ID.

If the message does not contain text describing an event, or if you cannot produce a suitable
event as JSON object for soem reason, do not return a JSON object. Instead, start your reply 
with the string "ERROR" (as very first word in all caps) and then explain the problem.
"""

def write_to_calendar( raw_msg ):
	msg = email.message_from_string(raw_msg, policy=email.policy.default)
	body = msg.get_body( preferencelist=('plain', 'html') ).get_content()
	msg_fmtd = textwrap.dedent( """\
		From: {msg['from']}
		To: {msg['to']} 
		Subject: {msg['subject']}
		Date: {msg['date']}
		Message-Id: {msg['message-id']} 

		{body}
		""" ).format( msg=msg, body=body )

	with open( "secrets.json" ) as f:
		secrets = json.load(f)

	client = openai.OpenAI( api_key=secrets["openai_key"] )

	chat_completion = client.chat.completions.create(
	    messages=[
    	    { "role": "system", "content": instructions },
        	{ "role": "user",   "content": msg_fmtd } ],
    	model="gpt-3.5-turbo",
	)		
	reply = chat_completion.choices[0].message.content
	try:
		event = json.loads( reply )
	except Exception as e:
		raise RuntimeError( "gpt replied: " + reply )
	add_event_to_calendar( event )


def add_event_to_calendar( event ):
	with open( "secrets.json" ) as f:
		secrets = json.load(f)
	service_account_file = '/home/anders/Downloads/calendar-additions-422517-c09da3cdda49.json'
	scopes = ['https://www.googleapis.com/auth/calendar']
	calendar_id = secrets["calendar_id"]

	credentials = service_account.Credentials.from_service_account_file(
    	service_account_file, scopes=scopes)
	service = build('calendar', 'v3', credentials=credentials)

	reply = service.events().insert(calendarId=calendar_id, body=event).execute()
	date = datetime.datetime.fromisoformat(event['start']['dateTime']).strftime('%-d %b %Y')
	
	subprocess.run([ "notify-send", "msg2gpt: Google Calendar event created", 
		f"{date}: {reply['summary']}" ])