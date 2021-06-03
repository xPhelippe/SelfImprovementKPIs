# imports for email
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import codecs
from .models import Person, QuestionAnswer, Survey
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings



def send_email(user_id):
    port = 465
    password = settings.EMAIL_PASS
    context = ssl.create_default_context()

    # find user
    try:
        user = Person.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return "Object does not exist"


    sender_email = "selfikpi@gmail.com"
    receiver_email = user.email
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:

        server.login("selfikpi@gmail.com",password)

        message = MIMEMultipart("alternative")
        message["Subject"] = "First User Test Email"
        message["From"] = sender_email

        text = """\
        this text won't render unless you have old tech. be cool
        """
        html = codecs.open("emails/singleSurvey.html",'r').read()

        # get most recent survey completion

        first_survey_id = Survey.objects.filter(user=user).first().id
        all_survey_answers = QuestionAnswer.objects.all().filter(survey=first_survey_id).order_by('time')
        most_recent_session_id = all_survey_answers.reverse()[0].sessionID
        most_recent_survey_responses = all_survey_answers.filter(sessionID=most_recent_session_id)


        # format email with results from most recent survey completion
        replacement_text = codecs.open("emails/singleSurveyReplacement.html",'r').read()
        
        for resp in most_recent_survey_responses:
            text = replacement_text.format(question=resp.question,response=resp.content)

            print("")
            print(html)
            html = html.replace("#!new rows here!#", text)

        html = html.replace("#!new rows here!#","")


        # add HTML to message
        part1 = MIMEText(text,"plain")
        part2 = MIMEText(html,"html")

        message.attach(part1)
        message.attach(part2)

        message["To"] = receiver_email

        server.sendmail(sender_email, receiver_email, message.as_string())