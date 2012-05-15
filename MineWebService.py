from mongoengine import *
from datetime import datetime
import smtplib
import string
from ftplib import FTP
DBNAME = 'test'
HOST = '76.181.68.191'
PORT = 27017

connect(DBNAME, host = HOST, port = PORT)

#class that holds relevant information for each database request
class Request(Document):
    studynumber = StringField(max_length=200)
    request_date = DateTimeField('Date Requested')
    processed = BooleanField()
    requestor = StringField(max_length = 200)

#posts the request to the database
def postRequest(studyid,  email, done=False):
    if not requestProcessed(studyid):
        post = Request(studynumber = studyid, request_date = datetime.now(), processed = done, requestor = email)
        post.save()

#returns true if studyid has been requested else returns false
def alreadyRequested(studyid):
    for request in Request.objects:
        if request.studynumber == studyid:
            return True
    return False

#returns true if studyid has been processed already
def requestProcessed(studyid):
    for request in Request.objects:
        if request.studynumber == studyid:
            if request.processed == False:
                return False
            return True

#marks each request for studyid processed and sends an email to each requestor
def markRequestDone(studyid):
    for request in Request.objects:
        if request.studynumber == studyid:
            if request.processed == False:
                request.processed = True
                request.save()
                sendEmail(request.requestor, studyid)

#returns a list of studyids as strings
def getStudyList():
    studylist = ['']
    for request in Request.objects:
        studylist.append(request.studynumber)
    studylist.remove('')
    return studylist

#returns true if GSID is valid else returns false
def isValidNumber(studyid):
    ftp = FTP('ftp.ncbi.nih.gov')
    ftp.login()
    ftp.cwd('/pub/geo/DATA/SeriesMatrix/')
    try:
        ftp.cwd(studyid)
    except:
        ftp.quit()
        return False

    ftp.quit()
    return True

#sends an email to the address specified
def sendEmail(address, studyid):
    MESSAGE = 'Your request for study ' + studyid + ' has been processed \n\n to view go to http://yates.webfactional.com/studies/'+studyid
    SENDER = 'noreply@yates.webfactional.com'
    SUBJECT = 'Mine has processed your study!'

    Body = string.join(( "From: %s" % SENDER,
                         "To: %s" % address,
                         "Subject: %s" % SUBJECT,
                         "",
                         MESSAGE
                         ), "\r\n")
    
    server = smtplib.SMTP('smtp.webfaction.com')
    server.login('minebox','b0d79559')
    server.sendmail(SENDER, [address], Body)
    server.quit()

#remove a specific request for a study by its id and the requestor
def remove(studyid, email):
    for request in Request.objects:
        if request.studynumber == studyid and request.requestor == email:
            request.delete()

#removes all requests for a specific study id
def removeBasedOnNumber(studyid):
    for request in Request.objects:
        if request.studynumber == studyid:
            request.delete()

#removes all requests made by a specific requestor
def removeBasedOnRequestor(email):
    for request in Request.objects:
        if request.requestor == email:
            request.delete()
            
