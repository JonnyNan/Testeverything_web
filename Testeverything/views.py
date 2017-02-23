from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.

def login(request):
    return render(request, 'login.html', {'name': 'login'})


@login_required
def index(request):
    # username = request.COOKIES.get('user', '')  # 读取浏览器cookie
    username = request.session.get('user', '')
    # return render(request, "index.html", {"user": username})
    return render(request, 'index.html', {'name': 'index'})


def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)  # 登录
        # response.set_cookie('user', username, 3600)  # 添加浏览器cookie
        request.session['user'] = username
        response = HttpResponseRedirect('/')
        return response
    else:
        return render(request, 'login.html', {'error': '账号或者密码不正确!'})


@login_required
def logout(request):
    auth.logout(request)  # 退出登录
    response = HttpResponseRedirect('/login/')
    return response
