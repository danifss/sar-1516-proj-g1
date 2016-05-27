from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_protect

from .models import User
from .forms import registerUserForm, loginForm

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

            user = authenticate(username=username, password=password)
            if user is not None:
                # get user and set session
                if user:
                    try:
                        utilizador = User.objects.get(username=username)
                        request.session['firstName'] = str(utilizador.firstName)
                        request.session['username'] = str(utilizador.username)
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
                request.session['firstName'] = "Visitante"
                request.session['loggedIn'] = False
                msgError ='The username and password are incorrect.'
    else:
        form = loginForm()

    request.session['firstName'] = "Visitante"
    request.session['loggedIn'] = False

    return render(request, 'core/login.html', {'form': form, 'error_message': msgError, \
                   'loggedIn' : request.session['loggedIn'], 'firstName': request.session['firstName']})


def authenticate(username, password):
    try:
        # validate if username exists
        user = User.objects.get(username=username)
    except:
        return None

    # validate password
    crypt = CryptoModule()

    salt = user.userSalt.decode('base64')
    web_pass = crypt.hashingSHA256(password, salt)
    bd_pass = user.password
    if bd_pass != web_pass:
        return False
    # all good
    return True


def logout(request):
    request.session['firstName'] = "Visitante"
    request.session['loggedIn'] = False
    template = loader.get_template('core/logout.html')
    return HttpResponse(template.render({'loggedIn': request.session['loggedIn'], 'firstName': request.session['firstName']}))


@csrf_protect
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

            # form.save(commit=False)

            # apply SHA256 to password
            salt_user = os.urandom(32)
            userSalt = salt_user.encode('base64')
            passwdHash = crypt.hashingSHA256(password, salt_user)
            # form.password = passwdHash

            # effectively registers new user in db
            # form.save()

            try:
                new_user = User(username=username, email=email, password=passwdHash, userSalt=userSalt,
                                firstName=firstName, lastName=lastName)
            except:
                msgError = "Error creating new User!"
                return render(request, 'core/register.html', {'form': form, 'error_message': msgError,
                              'loggedIn': request.session['loggedIn'], 'firstName': request.session['firstName']})

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
        return HttpResponse(template.render({'loggedIn' : request.session['loggedIn']}))

    try:
        user = User.objects.get(username=request.session['username'])

        context = RequestContext(request, {
            'username': user.username,
            'email': user.email,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'createdOn': user.createdOn,
            'loggedIn': request.session['loggedIn'],
        })

    except Exception as e:
        print "Error getting User details.", e
        return HttpResponseRedirect('/')

    template = loader.get_template('core/manage.html')
    return HttpResponse(template.render(context))

