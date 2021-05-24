from django.urls import path, include
from .views import defaultView, showMessages, askQuestion

urlpatterns = [
    path('', askQuestion),
    path('messages/',showMessages)
]