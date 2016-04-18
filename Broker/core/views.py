from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader


def index(request):
    template = loader.get_template('core/index.html')
    loggedIn = False
    if 'firstName' in request.session and 'loggedIn' in request.session:
        firstName = request.session['firstName']
        loggedIn = request.session['loggedIn']
    else:
        firstName = "Visitante"
        request.session['firstName'] = firstName
        request.session['loggedIn'] = False

    context = RequestContext(request, {
        'firstName': firstName,
        'loggedIn': loggedIn,
    })
    return HttpResponse(template.render(context))


def about(request):
    if 'loggedIn' not in request.session or request.session['loggedIn'] == False or 'username' not in request.session:
        request.session['firstName'] = "Visitante"
        request.session['loggedIn'] = False

    template = loader.get_template('core/about.html')
    return HttpResponse(template.render({'loggedIn': request.session['loggedIn'], 'firstName': request.session['firstName']}))
