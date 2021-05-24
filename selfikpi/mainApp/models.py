from django.db import models

# Create your models here.



#TODO find a way to use user class instead of custom class

class Person(models.Model):
    phoneNumber = models.CharField(max_length=12)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=40)

    def fullName(self):
        return str(firstName + " " + lastName)

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

    def __str__(self):
        return str(self.title)
    
    # TODO fix this function to not depend on the question ID 
    @property
    def first_question(self):
        return Question.objects.filter(survey__id=self.id).order_by('id').first()


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
        return str(content)