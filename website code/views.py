from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django import forms
from fetch.script import *
from datetime import datetime
import thread

from mongoengine import *

connect('test', host='76.181.68.191', port=27017)
#connect('test', host='140.254.202.193')

class ContactForm(forms.Form):
    email = forms.EmailField()
    gsid = forms.CharField()
    

class Study(Document):
    studynumber = StringField(max_length=200)
    request_date = DateTimeField('Date Requested')
    fetched = BooleanField()
    requestor = StringField(max_length = 200)

@csrf_protect
def home(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            
            if not Study.objects.filter(studynumber = form.cleaned_data['gsid']):

                data = Study(studynumber = form.cleaned_data['gsid'], request_date = datetime.now(), fetched = False, requestor = form.cleaned_data['email'])
                data.save()
                thread.start_new_thread(main,(form.cleaned_data['gsid'], None))
                return HttpResponse("Thanks for using M.I.N.E.") # Redirect after POST
            else:
                return HttpResponse("That study has already been requested")
    form = ContactForm() # An unbound form

    t = loader.get_template('studies/main.html')
    c = RequestContext(request, {'form':form,})
    return HttpResponse(t.render(c))

def data(request, studynumber):
    t = loader.get_template('studies/index.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))

def list(request):

    studylist = ['']
    for study in Study.objects:
        studylist.append(study.studynumber)
    studylist.remove('')
    t = loader.get_template('studies/list.html')
    c = RequestContext(request, {'studylist':studylist,})
    return HttpResponse(t.render(c))


    

