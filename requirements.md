# requirements for the document

requirements:
- store a single survey
- have the survey triggered once a day at a user-specified time
- record user responses to survey
- send summary email to user at end of week



## texting 
- [x] get a single responses from a user 
- [x] store the response of a random user 
- [x] store the responses of a unique user 
- [x] store a survey of questions related to a user 
- [x] let the user answer a question from the server
- [x] let the user answer the whole survey
- [ ] add introduction message
- [ ] allow user to end a conversation prematurely

## email
- [ ] generate a generic email that can be sent to the user
- [ ] populate email with data from one session
- [ ] aggregate data from a week and send it in an email

## timed sending
- [ ] set up a timer to send the email
- [ ] send a message to a arbitrary user at a specified time
- [ ] start a survey with a user at a specified time

## Allow user to modify their information
- [ ] allow the user to set the timer
- [ ] allow the user to create a survey
- [ ] allow the user to add questions to the survey
- [ ] allow the user to set the time a survey starts
- [ ] create user account from text

- [ ] create 'generic messages' table

# contents of response. POST:
```python
<QueryDict: {
    'ToCountry': ['US'], 
    'ToState': ['PA'], 
    'SmsMessageSid': ['SM519f8283b28d83024591ab0292b0bd34'], 
    'NumMedia': ['0'], 
    'ToCity': ['PHILADELPHIA'], 
    'FromZip': ['34292'], 
    'SmsSid': ['SM519f8283b28d83024591ab0292b0bd34'], 
    'FromState': ['FL'], 
    'SmsStatus': ['received'], 
    'FromCity': ['SARASOTA'], 
    'Body': ['Test'], 
    'FromCountry': ['US'], 
    'To': ['+12675329864'], 
    'ToZip': ['19110'], 
    'NumSegments': ['1'], 
    'MessageSid': ['SM519f8283b28d83024591ab0292b0bd34'], 
    'AccountSid': ['AC9c699500ef0938a95de018f957c0de3d'], 
    'From': ['+19417265904'], 
    'ApiVersion': ['2010-04-01']
}>
```



## Future Features

