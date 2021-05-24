from django.shortcuts import render
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import TextResponse, Person, Survey, QuestionAnswer, Question

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

@require_POST
@csrf_exempt
def askQuestion(request):
    # grabbing session ID if one exists
    sessionID = request.session.get('sessionID')

    print("found session id")

    # get the user connected to the phone 
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
