from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from user.models import User
from .models import Notebook

def check_login(function_view):

    def wrap(request, *args, **kw):
        # check session
        if request.session.get('username') and request.session.get('uid'):
            # return HttpResponse("Have already logged in")
            return function_view(request, *args, **kw)
        
        # check cookie
        cookie_username = request.COOKIES.get('username')
        cookie_uid = request.COOKIES.get('uid')
        if cookie_username and cookie_uid:
            # refill the session
            request.session['username'] = cookie_username
            request.session['uid'] = cookie_uid
            # return HttpResponse("Have already logged in")
            return function_view(request, *args, **kw)

        return HttpResponseRedirect('/user/login')
    return wrap

# Create your views here.

@check_login
def notebooks_view(request):
    username = request.session.get('username')
    try:
        user = User.objects.get(username=username)
    except Exception as e:
        return HttpResponse('There are some errors. Please login again.')
    
    notebooks = user.notebook_set.filter(is_active=True)

    return render(request, 'notebook/notebooks.html', locals())

@check_login
def add_view(request):
    # GET
    if request.method == "GET":
        return render(request, 'notebook/add.html')
    # POST
    elif request.method == "POST":
        uid = request.session['uid']
        title = request.POST['title']
        content = request.POST['content']

        Notebook.objects.create(title=title, content=content, is_active=True, user_id=uid)
        return HttpResponseRedirect('/notebook/notebooks')

@check_login
def update_view(request, notebook_id):

    try:
        notebook = Notebook.objects.get(id=notebook_id, is_active=True)
    except Exception as e:
        return HttpResponse('The note does not exist.')
    
    # GET
    if request.method == "GET":
        return render(request, 'notebook/update.html', locals())
    # POST
    elif request.method == "POST":

        title = request.POST['title']
        content = request.POST['content']
        
        notebook.title = title
        notebook.content = content

        notebook.save()

        return HttpResponseRedirect('/notebook/notebooks')

@check_login
def delete_view(request):

    notebook_id = request.GET.get('notebook_id')
    if not notebook_id:
        return HttpResponse('The note does not exist.')
    
    try:
        notebook = Notebook.objects.get(id=notebook_id, is_active=True)
    except Exception as e:
        return HttpResponse('The note does not exist.')
    
    notebook.is_active = False

    notebook.save()
    
    return HttpResponseRedirect('/notebook/notebooks')
