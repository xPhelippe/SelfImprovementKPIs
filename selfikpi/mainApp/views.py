from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from twilio.twiml.messaging_response import MessagingResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import TextResponse, Person, Survey, QuestionAnswer, Question

# imports for email
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import codecs
from django.urls import reverse


# Create your views here.

# this view saves a question from a user
@require_POST
@csrf_exempt
def defaultView(request):
    
    # get the content of the message
    body = request.POST['Body']
    phoneNumber=request.POST['From']

    # get the user connected to the phone 
    user = Person.objects.get(phoneNumber=phoneNumber)

    # save the content of the message to the database
    TextResponse.objects.create(message=body,userID=user).save()

    # creating message to return to user
    resp = MessagingResponse()
    resp.message("thanks for your message " + str(user.firstName))

    return HttpResponse(resp, content_type='application/xml')

# this view will ask the user a question and return its first request


@csrf_exempt
def sendEmail(request, email, user_id):
    port = 465
    password = "33simple"
    context = ssl.create_default_context()

    sender_email = "selfikpi@gmail.com"
    receiver_email = email
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:

        server.login("selfikpi@gmail.com",password)

        message = MIMEMultipart("alternative")
        message["Subject"] = "First User Test Email"
        message["From"] = sender_email

        text = """\
        this text won't render unless you have old tech. be cool
        """
        html = codecs.open("emails/singleSurvey.html",'r').read()

        print(html)
        # find user
        user = get_object_or_404(Person,id=user_id)
        print("user: " + str(user))

        # get most recent survey completion

        first_survey_id = Survey.objects.filter(user=user).first().id
        #print("first_survey_id: " + str(first_survey_id))

        all_survey_answers = QuestionAnswer.objects.all().filter(survey=first_survey_id).order_by('time')
        #print("all_survey_answers: " + str(all_survey_answers))

        #for resp in all_survey_answers:
        #    print(resp.time)

        most_recent_session_id = all_survey_answers.reverse()[0].sessionID
        #print("most_recent_session_id: " + str(most_recent_session_id))

        most_recent_survey_responses = all_survey_answers.filter(sessionID=most_recent_session_id)
        #print("most_recent_survey_responses: " + str(most_recent_survey_responses))

        #for resp in most_recent_survey_responses:
        #    print(str(resp.time) + " " + str(resp.question) + " " + str(resp.content))

        # populate html with question responses

        # #!new rows here!#

        replacement_text = codecs.open("emails/singleSurveyReplacement.html",'r').read()


        print(replacement_text)

        for resp in most_recent_survey_responses:
            text = replacement_text.format(question=resp.question,response=resp.content)

            print("")
            print(html)
            html = html.replace("#!new rows here!#", text)

        html = html.replace("#!new rows here!#","")

        print(html)

        # adding HTML to the message
        part1 = MIMEText(text,"plain")
        part2 = MIMEText(html,"html")

        message.attach(part1)
        message.attach(part2)

        message["To"] = receiver_email

        server.sendmail(sender_email, receiver_email, message.as_string())

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
