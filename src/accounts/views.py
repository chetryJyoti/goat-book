from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.contrib import messages
from accounts.models import Token
from django.urls import reverse
from django.contrib import auth,messages

def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse("login") + "?token=" + str(token.uid)
    )
    message_body = f"Use this link to log in:\n\n{url}"
    send_mail(
        'Your login link for Superlists',
         message_body,
        'jyotichetry087@gmail.com',
        [email],
    )
    messages.success(
        request,
        "Check your email, we've sent you a link you can use to log in."
    )
    return redirect("/")

def login(request):
    if user := auth.authenticate(uid=request.GET["token"]):
        auth.login(request, user)
    else:
        messages.error(request, "Invalid login link, please request a new one")
    return redirect("/")