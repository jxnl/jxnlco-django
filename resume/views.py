from django.shortcuts import render_to_response
from resume.models import Resume, Topic, Experience
from django.template import RequestContext

# Create your views here.

def resume(request):
    context = RequestContext(request)
    resume = Resume.objects.latest('id')
    context_dict = {}
    context_dict['resume'] = resume
    return render_to_response('resume/template_resume.html',
                              context_dict,
                              context)
