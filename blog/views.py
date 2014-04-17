from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from blog.models import Entry, Term
from django.core.exceptions import ObjectDoesNotExist


def home(request):
    context = RequestContext(request)
    entry = Entry.objects.latest('start_date')
    term = entry.term
    context_dict = {}
    context_dict['entry'] = entry
    context_dict['term'] = term
    return render_to_response('blog/template_home.html', context_dict, context)


def post(request, style, key):
    context = RequestContext(request)
    entry = get_object_or_404(Entry, pk=key)
    context_dict = {}
    context_dict['entry'] = entry
    try:
        context_dict['next'] = entry.get_next_by_start_date()
    except ObjectDoesNotExist:
        pass
    try:
        context_dict['prev'] = entry.get_previous_by_start_date()
    except ObjectDoesNotExist:
        pass
    return render_to_response('blog/template_post.html', context_dict, context)

def archive(request):
    """ Generates Projects Pages"""
    context = RequestContext(request)
    context_dict = {}
    context_dict["terms"] = Term.objects.reverse()
    context_dict['recent_entry'] = Entry.objects.latest('start_date')
    return render_to_response('blog/template_archive.html', context_dict,
                              context)


def blog(request):
    """ Generates Projects Pages"""
    context = RequestContext(request)
    cur_term = Term.objects.latest('pk')
    context_dict = {}
    context_dict['cur_term'] = cur_term
    context_dict['recent_entry'] = Entry.objects.latest('start_date')
    return render_to_response('blog/template_blog.html', context_dict, context)


def projects(request):
    """ Generates Projects Pages"""
    context = RequestContext(request)
    projects_list = Entry.objects.exclude(style='writing')
    new_list = [projects_list[i:i + 3]
                for i in range(0, len(projects_list), 3)]
    context_dict = {}
    context_dict['projects_list'] = new_list
    return render_to_response('blog/template_project.html',
                              context_dict, context)


def about(request):
    context = RequestContext(request)
    context_dict = {}
    return render_to_response('blog/template_about.html',
                              context_dict, context)
