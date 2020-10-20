# CalendlyGoogleCalendar

### Purpose of this git repo
To automate the process of blocking my day after x events have been already scheduled on my calendar. 

My specific use case:

There are events that get scheduled on my calendar by Calendly. Let's say I am available for 5 hours; however, I can take 3 events spread over in those 5 hours. 
Therefore, whenever a calendly event is scheduled/updated/declined, AWS Lambda triggers my python script. 


DISCLAIMER: 
You will need to connect your Google Calendar first via Google [Calendar API](https://developers.google.com/calendar).

I have built this file keeping my specific use case in mind; however, if there's anything you feel I can help to generalize - please let me know. 
