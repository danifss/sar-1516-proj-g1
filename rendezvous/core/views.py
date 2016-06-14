from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
# from django.views.decorators.csrf import csrf_protect

from .models import User, Service, Broker
from .forms import loginForm, addBrokerForm

import os
from CryptoModule import *


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

    return HttpResponse(template.render({'firstName': firstName, 'loggedIn': loggedIn, }))


def about(request):
    if 'loggedIn' not in request.session or request.session['loggedIn'] == False or 'username' not in request.session:
        request.session['firstName'] = "Visitante"
        request.session['loggedIn'] = False

    template = loader.get_template('core/about.html')
    return HttpResponse(template.render({'loggedIn': request.session['loggedIn'], 'firstName': request.session['firstName']}))


def login(request):
    if 'loggedIn' not in request.session or request.session['loggedIn'] == False or 'username' not in request.session:
        request.session['firstName'] = "Visitante"
        request.session['loggedIn'] = False

    msgError = ''
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid:
            username = str(request.POST['username'])  # str(form.cleaned_data['username'])
            password = str(request.POST['password'])  # str(form.cleaned_data['password'])

            user, valid = authenticate(username=username, password=password)
            if user is not None:
                # get user and set session
                if valid:
                    try:
                        # utilizador = User.objects.get(username=username)
                        request.session['firstName'] = str(user.firstName)
                        request.session['username'] = str(user.username)
                        request.session['loggedIn'] = True
                    except Exception as e:
                        print "Some error acurred getting user to logging in.", e
                        request.session['firstName'] = "Visitante"
                        request.session['loggedIn'] = False
                        return HttpResponseRedirect('/login/')
                    return HttpResponseRedirect('/')
                else:
                    request.session['firstName'] = "Visitante"
                    request.session['loggedIn'] = False
                    msgError = 'The password is incorrect!'
            else:
                # the authentication system was unable to verify the username and password
                msgError ='The username and password are incorrect.'
                request.session['firstName'] = "Visitante"
                request.session['loggedIn'] = False
    else:
        form = loginForm()
        request.session['firstName'] = "Visitante"
        request.session['loggedIn'] = False

    return render(request, 'core/login.html', {'form': form, 'error_message': msgError,
                                               'loggedIn': request.session['loggedIn'],
                                               'firstName': request.session['firstName']})


def authenticate(username, password):
    try:
        # validate if username exists
        user = User.objects.get(username=username)
    except:
        return None, None

    # validate password
    crypt = CryptoModule()

    salt = user.userSalt.decode('base64')
    web_pass = crypt.hashingSHA256(password, salt)
    bd_pass = user.password
    if bd_pass != web_pass:
        return user, False
    # all good
    return user, True


def logout(request):
    request.session['firstName'] = "Visitante"
    request.session['loggedIn'] = False
    template = loader.get_template('core/logout.html')
    return HttpResponse(template.render({'loggedIn': request.session['loggedIn'], 'firstName': request.session['firstName']}))


def services(request):
    if 'loggedIn' not in request.session or request.session['loggedIn'] == False or 'username' not in request.session:
        request.session['firstName'] = "Visitante"
        request.session['loggedIn'] = False
        template = loader.get_template('core/index.html')
        return HttpResponse(template.render({'loggedIn': request.session['loggedIn'],
                                             'firstName': request.session['firstName']}))
    try:
        services = Service.objects.all()
        context = {
            'services': services,
            'loggedIn': request.session['loggedIn'],
            'firstName': request.session['firstName'],
        }
    except Exception as e:
        print "Error getting Content.", e
        return HttpResponseRedirect('/')

    template = loader.get_template('core/services.html')
    return HttpResponse(template.render(context))


# @csrf_protect
def brokers(request):
    if 'loggedIn' not in request.session or request.session['loggedIn'] == False or 'username' not in request.session:
        request.session['firstName'] = "Visitante"
        request.session['loggedIn'] = False
        template = loader.get_template('core/index.html')
        return HttpResponse(template.render({'loggedIn': request.session['loggedIn'],
                                             'firstName': request.session['firstName']}))

    action_link = 'core/action_handler.html'
    context = {
        'loggedIn': request.session['loggedIn'],
        'firstName': request.session['firstName'],
        'page_title': 'Brokers (PSWs)',
        'link_back': '/brokers',
    }
    try:
        brokers_list = Broker.objects.all()
        context.update({
            'brokers': brokers_list,
        })
    except Exception as e:
        print "Error getting Content.", e
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = addBrokerForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username=request.session['username'])
                name = form.cleaned_data['name']
                ip = form.cleaned_data['ip']
                description = form.cleaned_data['description']
                new_broker = Broker(user=user, name=name, ip=ip, description=description)
                new_broker.save()
                infoMessage = "You successfully added a new Broker!"
                context.update({
                    'result': True,
                    'info_message': infoMessage,
                })
                # template = loader.get_template('core/broker_add.html')
                return render(request, action_link, context)
            except:
                infoMessage = "Something happened while adding the new Broker!"
                msgError = "Error adding new Broker."
                context.update({
                    'form': form,
                    'result': False,
                    'info_message': infoMessage,
                    'error_message': msgError,
                    'collapse': 'in',
                })
        else:
            msgError = "Invalid Broker information!"
            context.update({
                'brokers': brokers_list,
                'form': form,
                'result': False,
                'error_message': msgError,
                'loggedIn': request.session['loggedIn'],
                'firstName': request.session['firstName'],
                'collapse': 'in',
            })
    else:
        form = addBrokerForm()
        context.update({
            'form': form,
        })

    # template = loader.get_template('core/brokers.html')
    # return HttpResponse(template.render(context))
    return render(request, 'core/brokers.html', context)


def broker_del(request, pk=None):
    if 'loggedIn' not in request.session or request.session['loggedIn'] == False or 'username' not in request.session:
        request.session['firstName'] = "Visitante"
        request.session['loggedIn'] = False
        template = loader.get_template('core/index.html')
        return HttpResponse(template.render({'loggedIn': request.session['loggedIn'],
                                             'firstName': request.session['firstName']}))

    action_link = 'core/action_handler.html'
    context = {
        'loggedIn': request.session['loggedIn'],
        'firstName': request.session['firstName'],
        'page_title': 'Brokers (PSWs)',
        'link_back': '/brokers',
    }
    if pk is not None:
        try:
            id = int(pk)
            broker = Broker.objects.get(brokerID=id)
            broker.delete()
            infoMessage = "You successfully deleted the Broker!"
            context.update({
                'result': True,
                'info_message': infoMessage,
            })
        except:
            infoMessage = "Something happened while deleting the Broker!"
            msgError = "Invalid Broker!"
            context.update({
                'result': False,
                'info_message': infoMessage,
                'error_message': msgError,
            })
    else:
        return HttpResponseRedirect('/')

    template = loader.get_template(action_link)
    return HttpResponse(template.render(context))


def service_del(request, pk=None):
    if 'loggedIn' not in request.session or request.session['loggedIn'] == False or 'username' not in request.session:
        request.session['firstName'] = "Visitante"
        request.session['loggedIn'] = False
        template = loader.get_template('core/index.html')
        return HttpResponse(template.render({'loggedIn': request.session['loggedIn'],
                                             'firstName': request.session['firstName']}))

    action_link = 'core/action_handler.html'
    context = {
        'loggedIn': request.session['loggedIn'],
        'firstName': request.session['firstName'],
        'page_title': 'Services',
        'link_back': '/services',
    }
    if pk is not None:
        try:
            id = int(pk)
            service = Service.objects.get(serviceID=id)
            service.delete()
            infoMessage = "You successfully deleted the Service!"
            context.update({
                'result': True,
                'info_message': infoMessage,
            })
        except:
            infoMessage = "Something happened while deleting the Service!"
            msgError = "Invalid Service!"
            context.update({
                'result': False,
                'info_message': infoMessage,
                'error_message': msgError,
            })
    else:
        return HttpResponseRedirect('/')

    template = loader.get_template(action_link)
    return HttpResponse(template.render(context))


def services_update(request):
    if 'loggedIn' not in request.session or request.session['loggedIn'] == False or 'username' not in request.session:
        request.session['firstName'] = "Visitante"
        request.session['loggedIn'] = False
        template = loader.get_template('core/index.html')
        return HttpResponse(template.render({'loggedIn': request.session['loggedIn'],
                                             'firstName': request.session['firstName']}))

    action_link = 'core/services.html'
    context = {
        'loggedIn': request.session['loggedIn'],
        'firstName': request.session['firstName'],
    }
    try:
        #TODO connect to all existent brokers to ask for their services and then save them
        services = Service.objects.all()
        context.update({
            'services': services,
        })
    except Exception as e:
        print ("Error getting Content.")
        return HttpResponseRedirect('/')

    template = loader.get_template(action_link)
    return HttpResponse(template.render(context))
