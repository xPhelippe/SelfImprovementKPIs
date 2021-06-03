from django.db import models
from django.utils import timezone
from timezone_field import TimeZoneField

import redis
import arrow
# Create your models here.



#TODO find a way to use user class instead of custom class

class Person(models.Model):
    phoneNumber = models.CharField(max_length=12)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=40)
    email = models.CharField(max_length=40,null=True,blank=True)

    def fullName(self):
        return str(self.firstName + " " + self.lastName)

    def __str__(self):
        return str(self.firstName + " " +  self.lastName)
    

# TODO get rid of this 
# stores the user's text response 
class TextResponse(models.Model):
    message = models.CharField(max_length=200)
    userID = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='texts',default=1)

    def __str__(self):
        return str(self.message)

# relates a specific survey to a user
class Survey(models.Model):
    user = models.ForeignKey(Person,on_delete=models.CASCADE, related_name='survey')
    title = models.CharField(max_length=50)
    reminderTime = models.DateTimeField(blank=True,null=True)
    timezone = TimeZoneField(default='UTC', null=True, blank=True)
    task_id = models.CharField(max_length=50, blank=True,null=True)
    emailTime = models.DateTimeField(blank=True,null=True)


    def __str__(self):
        return str(self.title)
    
    # TODO fix this function to not depend on the question ID 
    @property
    def first_question(self):
        return Question.objects.filter(survey__id=self.id).order_by('id').first()

    def schedule_reminder(self):

        # create delay until reminder time
        print("creating delay until reminder time:")
        reminder_time = arrow.get(self.reminderTime)
        print("reminder_time: " + str(reminder_time))
        now = arrow.now(self.timezone)
        print("now: " + str(now))
        print(str((reminder_time-now).total_seconds()))
        milli_to_wait = int((reminder_time - now).total_seconds())*1000

        print("Millis to wait: " + str(milli_to_wait))

        # Schedule task

        print("Scheduling task")
        from .tasks import send_survey_reminder

        result = send_survey_reminder.send_with_options(
            args = (self.id,),
            delay=milli_to_wait
        )

        return result.options['redis_message_id']

    def cancel_task(self):
        print("canceling task")
        redis_client = redis.Redis(host="127.0.0.1", port=6379, db=0)
        redis_client.hdel("dramatiq:default.DQ.msgs", self.task_id)



    def save(self, *args, **kwargs):

        print("finding previous task")
        if self.task_id:
            print("found previous task")
            self.cancel_task()

        print("saving new survey")
        super(Survey, self).save(*args,**kwargs)

        print("Scheduling reminder")
        self.task_id = self.schedule_reminder()

        print("saving new survey again")
        super(Survey, self).save(*args, **kwargs)


class Question(models.Model):

    qtypes = (
        (0, "TEXT"),
        (1, "SCALE"),
        (2, "YESORNO")
    )

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='question')
    text = models.CharField(max_length=200)
    qtype = models.IntegerField(choices=qtypes)
    nextquestion = models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return str(self.text)



# answer question model
# - session ID
# - content
# - time 
# - user 
# - survey
# - question

class QuestionAnswer(models.Model):

    sessionID = models.CharField(max_length=20)
    content = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True,auto_now=False)
    user = models.ForeignKey(Person,on_delete=models.CASCADE, related_name="questionanswer")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='questionanswer')
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questionanswer')

    def __str__(self):
        return str(self.content)