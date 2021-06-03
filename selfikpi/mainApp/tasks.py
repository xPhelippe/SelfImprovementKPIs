import dramatiq
from twilio.rest import Client
from django.conf import settings
from .models import Survey, Person
from django.core.exceptions import ObjectDoesNotExist
from . import helper

# imports for email
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import codecs

import arrow

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

# dramatiq actor for sending message

@dramatiq.actor
def send_survey_reminder(survey_id):


    print("retreiving survey with id: " + str(survey_id))
    survey = Survey.objects.get(id=survey_id)

    print("retrieving user for survey: " + str(survey.user.id))
    user = Person.objects.get(id=survey.user.id)

    print("sending message")
    body = "Hi {0}! Would you like to talk about your day? Respond with \"survey {1}\" to start your survey".format(
        user.firstName,
        survey.title.replace(" ","-")
    )

    mesg = client.messages.create(
        body=body,
        to=user.phoneNumber,
        from_=settings.TWILIO_NUMBER
    )

    # update data entry for task (this will create a new task)
    # repeats daily currently
    # TODO change repetition to a user-defined time interval

    old_reminder_time = arrow.get(survey.reminderTime, survey.timezone)

    new_reminder_time = old_reminder_time.shift(hours=24)

    survey.reminderTime = new_reminder_time.format()

    survey.save()


# TODO change this to make an internal request to the view that already does this
@dramatiq.actor
def sendWeeklyEmail(user_id):


    # send the weekly email
    helper.send_weekly_email(user_id)

    # set the new time for the next email
    survey = Survey.objects.get(user=user_id)
    

    
    
        

    




    
