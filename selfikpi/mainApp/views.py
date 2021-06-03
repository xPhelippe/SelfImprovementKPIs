from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from twilio.twiml.messaging_response import MessagingResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import TextResponse, Person, Survey, QuestionAnswer, Question
from . import tasks
from django.conf import settings
from . import helper

# imports for email
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import codecs
from django.urls import reverse


@csrf_exempt
def testTimed(request):
    survey_id = request.POST["survey_id"]

    tasks.send_survey_reminder(survey_id)



@csrf_exempt
def sendEmail(request, user_id):
    try:
        helper.send_weekly_email(user_id)
    except ObjectDoesNotExist:
        resp =MessagingResponse()
        resp.message("Internal Error")
        
        return HttpResponse(resp,content_type='application/xml')

    resp = MessagingResponse()
    resp.message("Email sent")
        
    return HttpResponse(resp, content_type='application/xml')

@require_POST
@csrf_exempt
def askQuestion(request):
    # grabbing session ID if one exists
    sessionID = request.session.get('sessionID')

    print("found session id")

    # grab user account
    phoneNumber=request.POST['From']
    user = Person.objects.get(phoneNumber=phoneNumber)

    print("found user")

    if sessionID:
        # grabbing response from previous question code
        qresponse = request.POST['Body']

        # grab question that was answered
        question = Question.objects.get(id=request.session['questionID'])

        # creating response in database
        qans = QuestionAnswer.objects.create(
            sessionID=request.session['sessionID'],
            content=qresponse,
            user=user,
            question = question,
            survey = question.survey
        )

        # grabbing the next question
        if question.nextquestion:

            # grabbing next question
            qnext = Question.objects.get(id=question.nextquestion.id)
            request.session['questionID'] = qnext.id

            print(qnext)

            # creating response 
            # creating and sending response
            resp = MessagingResponse()
            resp.message(qnext.text)
        else:

            # deleting session information
            del request.session['sessionID']
            del request.session['questionID']

            # creating and sending response
            resp = MessagingResponse()
            resp.message("thank you for taking your time to answer this survey.")

    else:

        body = request.POST['Body']

        if body == "email":

            redirectUrl = reverse("sendEmail", 
                                    kwargs={
                                        'email':user.email,
                                        'user_id':user.id})

            return HttpResponseRedirect(redirectUrl)

                    

        # get the first question of the survey
        firstQuestion = Survey.objects.get(user=user).first_question
        request.session['questionID'] = firstQuestion.id 
        print("grabbed first question")

        # create the session id for this survey
        sessionID = request.POST['MessageSid'][2:11]
        request.session['sessionID'] = sessionID
        print("created session id")

        # creating and sending response
        resp = MessagingResponse()
        resp.message(firstQuestion.text)

    
    return HttpResponse(resp, content_type='application/xml')

def showMessages(request):
    messages = QuestionAnswer.objects.all()

    return render(request, 'index.html', {'texts':messages})


