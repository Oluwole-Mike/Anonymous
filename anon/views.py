from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from . models import *

# Create your views here.


def Home(request):
    try:
        return render(request, "index.html")

    except Exception as ex:
        print(ex)




def AddAnonymousMessage(request, id):
    get_user = User.objects.get(pk=id)

    try:
        if request.method=='POST':
            message = request.POST["message"]

            if len(message) != 0:
                add_anonymous_message = AnonymousMessage(
                    message=message,
                    user=get_user
                    )
                add_anonymous_message.save()

                messages.success(request, f'Secret message has been sent to {get_user.username}')
                return redirect("home")
            return redirect("add-anonymous-message")

        else:
            return render(request, "add_message.html", {"get_user": get_user})
            # return redirect(reverse('add-anonymous-message', kwargs={"username": get_user}))

    except Exception as ex:
        print(ex)




def AllAnonymousMessage(request):
    try:
        all_anonymous_message = AnonymousMessage.objects.filter(user_id = request.user) #.order_by('-date_created').values()
        return render(request, "all_message.html", {"all_anonymous_messages": all_anonymous_message})

    except Exception as ex:
        print(ex)




def Register(request):
    try:
        if request.method=='POST':
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']

            if password==confirm_password:                                
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username taken')
                    return redirect("register")  
                
                else:
                    user = User.objects.create_user(
                        username=username,
                        email=email,  
                        password=password
                        )
                    user.save()

                    messages.success(request, 'Account created. Please log in')
                    return render(request, "login.html", {"user": user}) 

            else:
                messages.error(request, 'Password not the same')
                return redirect("register") 
            
        elif request.method=='GET': 
            return render(request, "register.html") 

    except Exception as ex:
        print(ex)    




def Login(request):
    try:
        if request.method=='POST':
            username = request.POST['username']
            password = request.POST['password']
            
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)

                request.session["userId"] = user.id
                request.session["username"] = user.username
                request.session["email"] = user.email

                return redirect("home")
            
            else:
                messages.error(request, 'Incorrect username or password')
                return render(request, "login.html") 
            
        elif request.method=='GET':
            return render(request, "login.html") 
                
    except Exception as ex:
        print(ex)




def Logout(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        del request.session[key]
    auth.logout(request)
    return redirect("home")