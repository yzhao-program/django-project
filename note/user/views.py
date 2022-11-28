from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import User
import hashlib

# Create your views here.
def register_view(request):

    # GET
    if request.method == "GET":
        return render(request, "user/register.html")

    # POST
    elif request.method == "POST":

        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return HttpResponse("Two passwords didn't match.")

        existing_users = User.objects.filter(username=username)

        if existing_users:
            return HttpResponse("This username has already been registered.")
        
        m = hashlib.md5()
        m.update(password1.encode())
        password_m = m.hexdigest()

        try:
            user = User.objects.create(username=username, password=password_m)
        except Exception as e:
            return HttpResponse("This username has already been registered.")

        # let user be login status after successful register
        request.session['username'] = username
        request.session['uid'] = user.id

        # return HttpResponse("Register Successfully.")
        return HttpResponseRedirect('/index')

def login_view(request):
    # GET
    if request.method == "GET":

        # check session
        if request.session.get('username') and request.session.get('uid'):
            # return HttpResponse("Have already logged in")
            return HttpResponseRedirect('/index')
        
        # check cookie
        cookie_username = request.COOKIES.get('username')
        cookie_uid = request.COOKIES.get('uid')
        if cookie_username and cookie_uid:
            # refill the session
            request.session['username'] = cookie_username
            request.session['uid'] = cookie_uid
            # return HttpResponse("Have already logged in")
            return HttpResponseRedirect('/index')

        return render(request, "user/login.html")
    # POST
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except Exception as e:
            return HttpResponse('Username or password is wrong.')
        
        m = hashlib.md5()
        m.update(password.encode())

        if m.hexdigest() != user.password:
            return HttpResponse('Username or password is wrong.')
        
        # let user be login status after successful login
        request.session['username'] = username
        request.session['uid'] = user.id
        
        # resp = HttpResponse("Login Successfully.")
        resp = HttpResponseRedirect('/index')

        if request.POST.get('check', 'off') == 'on':
            resp.set_cookie('username', username, 60*60*24*30)
            resp.set_cookie('uid', user.id, 60*60*24*30)

        return resp

def logout_view(request):

    # delete the information in session
    if 'username' in request.session:
        del request.session['username']
    if 'uid' in request.session:
        del request.session['uid']
    
    # delete the information in cookie
    resp = HttpResponseRedirect('/index')
    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    if 'uid' in request.COOKIES:
        resp.delete_cookie('uid')
    
    return resp
