from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
import os
from Testeverything.models import ApiTestCase


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


def upload_file(request):
    if request.method == "POST":  # 请求方法为POST时，进行处理
        myFile = request.FILES.get("myfile", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return HttpResponse("没有文件要上传！")
        baseDir = os.path.dirname(os.path.abspath(__name__));
        uploaddir = os.path.join(baseDir, 'upload');
        destination = open(os.path.join(uploaddir, myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        # 写入数据
        filename = myFile.name.split(".")[-2];
        ApiTestCase.objects.get_or_create(name=filename, case_abspath=uploaddir+"/"+myFile.name);


        return HttpResponse("上传完成!你可以去接口测试里执行")



def api_test(request):
    api_test_case_list = ApiTestCase.objects.all()
    return render(request, 'apitest.html',{"apiTestCaseList":api_test_case_list})


def add_api_test(request):
    return render(request, 'createapicase.html')


def delete_test(request,case_id):
    file_path = ApiTestCase.objects.get(id=case_id).case_abspath
    os.remove(file_path);

    ApiTestCase.objects.get(id=case_id).delete()

    api_test_case_list = ApiTestCase.objects.all()
    return render(request, 'apitest.html',{"apiTestCaseList":api_test_case_list})


def run_api_test(request,case_id):
    file_path = ApiTestCase.objects.get(id=case_id).case_abspath
    os.system('zsh && httprunner '+file_path)


    api_test_case_list = ApiTestCase.objects.all()
    return render(request, 'apitest.html',{"apiTestCaseList":api_test_case_list})







@login_required
def api_request(request):
    return render(request, 'request.html')


@login_required
def logout(request):
    auth.logout(request)  # 退出登录
    response = HttpResponseRedirect('/login/')
    return response
