from django.urls import path, include
from .views import defaultView, showMessages, askQuestion, sendEmail

urlpatterns = [
    path('', askQuestion),
    path('messages/',showMessages),
    path('sendEmail/<str:email>/<int:user_id>/',sendEmail,name='sendEmail')
]