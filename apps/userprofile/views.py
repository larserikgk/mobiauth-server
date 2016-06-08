from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def index(request):
    if request.user.is_authenticated():
        template = loader.get_template('userprofile/index_authenticated.html')
    else:
        template = loader.get_template('userprofile/index.html')
    context = {
        'user': request.user,
    }
    return HttpResponse(template.render(context, request))
