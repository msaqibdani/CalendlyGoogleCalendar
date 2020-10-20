from calendly import Calendly
import datetime
import pickle
import os.path
from os import path
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# maximum number of Caledly events for that day
LIMIT = 4 



# gets the email address and name of the person event assigned to
def getExtendedAssignedDetails(events):
	return events['payload']['event']['extended_assigned_to'][0]

# gets the start date of the event
def getStartDate(events):
	return events['payload']['event']['start_time'].split('T')[0]

#initializes token (connect to Google Calendar)
def initializeToken():

		SCOPES = ['https://www.googleapis.com/auth/calendar']

		CREDENTIALS_FILE = './credentials.json'
		creds = None

		if os.path.exists('token.pickle'):
			with open('token.pickle', 'rb') as token:
				creds = pickle.load(token)

		if not creds or not creds.valid:
			if creds and creds.expired and creds.refresh_token:
				creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES, redirect_uri = 'http://localhost:8000/index/callback')
				creds = flow.run_local_server(port=8001)

			with open('token.pickle', 'wb') as token:
				pickle.dump(creds, token)

		service = build('calendar', 'v3', credentials=creds)
		return service
	
#return all the events for the day
def getAllEventsForToday(service, date):
	return service.events().list(calendarId='primary', timeMin=date+'T00:00:00-04:00', timeMax=date+'T23:59:59-04:00', singleEvents=True, orderBy='startTime').execute()

#Count how many admission session events 
def countSWERobinEvents(events, date):
	count = 0
	blocking_all_day = False
	for event in getAllEventsForToday(service, date)['items']:
		
		# -> Has your day been already blocked
		if 'summary' in event and event['summary'] == 'Blocking_All_Day':
			blocking_all_day = True


		if 'summary' in event and 'description' in event and 'start' in event:		# -> For Round Robin SWE Events:
			summary_first_half = event['summary'].split(':')[0] 					# -> Always should yield: Pathrise Session
			
			event_description = event['description'].split(':')
			if len(event_description) >= 2:
				description_first_half = event['description'].split(':')[1] 		# -> Always should yield: SWE Mentoring 1
			start_date = event['start']['dateTime'].split('T')[0] 					# -> Always should yield: Today's Date

			# -> if it's the particlar type of event that you want to count for. In other words, avoid other events
			if summary_first_half == 'Pathrise Session' and description_first_half == ' SWE Mentoring 1' and start_date == date:
				count += 1

	return count, blocking_all_day


# Create a new event 
def createNewEvent(service, date):
	new_event = {
		'summary': 'Blocking_All_Day',
  		'location': '',
  		'description': 'To not allow Pathrise to schedule anymore events for the day',
  		'start': {
  			'dateTime': date+'T00:00:00-04:00',
    		'timeZone': 'America/Indianapolis',
  		},
  		'end': {
    		'dateTime': date+'T23:59:59-04:00',
    		'timeZone': 'America/Indianapolis',
  		},
	}

	event = service.events().insert(calendarId='primary', body=new_event).execute()




count, state = countSWERobinEvents(service, date)
if not state and count == LIMIT:
	createNewEvent(service, date)


