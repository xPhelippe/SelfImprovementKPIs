from django.urls import path, include
from .views import showMessages, askQuestion, sendEmail, testTimed

urlpatterns = [
    path('', askQuestion),
    path('messages/',showMessages),
    path('sendEmail/<int:user_id>/',sendEmail,name='sendEmail'),
    path('test/',testTimed,name='test')
]