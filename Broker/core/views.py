from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
# from django.views.decorators.csrf import csrf_protect

from .models import User, Service, Broker
from .forms import registerUserForm, loginForm, addBrokerForm

import os
from CryptoModule import *
import requests
from requests import exceptions


host = 'http://localhost:9000/' # 10.1.1.2


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


# @csrf_protect
def register(request):
    if 'loggedIn' not in request.session or request.session['loggedIn'] == False or 'username' not in request.session:
        request.session['firstName'] = "Visitante"
        request.session['loggedIn'] = False

    if request.method == 'POST':
        form = registerUserForm(request.POST)
        if form.is_valid():

            # instantiate Crypto Module
            crypt = CryptoModule()

            email = str(form.cleaned_data['email'])
            password = str(form.cleaned_data['password2'])
            username = str(form.cleaned_data['username'])
            firstName = str(form.cleaned_data['lastName'])
            lastName = str(form.cleaned_data['firstName'])

            try:
                existUser1 = User.objects.get(username=username)
                existUser2 = User.objects.get(email=email)

                if existUser1 is not None or existUser2 is not None:
                    msgError = "This username or email is already registered!"
                    form = registerUserForm(request.POST)
                    return render(request, 'core/register.html', {'form': form, 'error_message': msgError,
                                  'loggedIn': request.session['loggedIn'], 'firstName': request.session['firstName']})
            except:
                pass

            # apply SHA256 to password
            salt_user = os.urandom(32)
            userSalt = salt_user.encode('base64')
            passwdHash = crypt.hashingSHA256(password, salt_user)

            try:
                new_user = User(username=username, email=email, password=passwdHash, userSalt=userSalt,
                                firstName=firstName, lastName=lastName)
            except:
                msgError = "Error creating new User!"
                return render(request, 'core/register.html', {'form': form, 'error_message': msgError,
                              'loggedIn': request.session['loggedIn'], 'firstName': request.session['firstName']})

            # Save the new user into the database
            new_user.save()

            return HttpResponseRedirect('../login/')
    else:
        form = registerUserForm()

    return render(request, 'core/register.html', {'form': form,
                  'loggedIn': request.session['loggedIn'], 'firstName': request.session['firstName']})


def accountManage(request):
    if 'loggedIn' not in request.session or request.session['loggedIn'] == False or 'username' not in request.session:
        request.session['firstName'] = "Visitante"
        request.session['loggedIn'] = False
        template = loader.get_template('core/index.html')
        return HttpResponse(template.render({'loggedIn': request.session['loggedIn']}))

    try:
        user = User.objects.get(username=request.session['username'])

        context = {
            'username': user.username,
            'email': user.email,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'createdOn': user.createdOn,
            'loggedIn': request.session['loggedIn'],
        }

    except Exception as e:
        print "Error getting User details.", e
        return HttpResponseRedirect('/')

    template = loader.get_template('core/manage.html')
    return HttpResponse(template.render(context))


def services(request):
    if 'loggedIn' not in request.session or request.session['loggedIn'] == False or 'username' not in request.session:
        request.session['firstName'] = "Visitante"
        request.session['loggedIn'] = False
        template = loader.get_template('core/index.html')
        return HttpResponse(template.render({'loggedIn': request.session['loggedIn'],
                                             'firstName': request.session['firstName']}))
    try:
        # services = Service.objects.all()
        services = None
        url = host + 'api/services/'
        result, status = proxy(path=url, method='GET')
        if status == 200:
            services = result['results']

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


def proxy(path=None, method='GET', data=None):
    timeout = 60 * 5

    r = None
    # 501 Not Implemented
    response = None
    try:
        if method == 'GET':
            r = requests.get(path, data=data, timeout=timeout)
        elif method == 'POST':
            r = requests.post(path, data=data, timeout=timeout)
        elif method == 'PUT':
            r = requests.put(path, data=data, timeout=timeout)
        elif method == 'DELETE':
            r = requests.delete(path, data=data, timeout=timeout)

    except exceptions.Timeout:
        # 504 Gateway Timeout
        response = None
    except exceptions.ConnectionError:
        # 503 Service Unavailable
        response = None

    if r is not None:
        if r.headers.get('Content-Type', None) == 'application/json':
            response = (r.json(), r.status_code)
        else:
            response = (r.text, r.status_code)
    return response

