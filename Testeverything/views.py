from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
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


@login_required
def upload_file(request):
    if request.method == "POST":  # 请求方法为POST时，进行处理
        my_file = request.FILES.get("my_file", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not my_file:
            return render(request, 'createApiCase.html', {'error': '没有找到你要上传的文件!'})
        base_dir = os.path.dirname(os.path.abspath(__name__));
        upload_dir = os.path.join(base_dir, 'upload');
        destination = open(os.path.join(upload_dir, my_file.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in my_file.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        # 写入数据
        filename = my_file.name.split(".")[-2];
        ApiTestCase.objects.get_or_create(name=filename, case_abspath=upload_dir + "/" + my_file.name);

        return render(request, 'createApiCase.html', {'success': '上传文件成功!'})


@login_required
def api_test(request):
    api_test_case_list = ApiTestCase.objects.all()
    return render(request, 'apiTest.html', {"apiTestCaseList": api_test_case_list})


@login_required
def add_api_test(request):
    return render(request, 'createApiCase.html')


@login_required
def delete_test(request, case_id):
    file_path = ApiTestCase.objects.get(id=case_id).case_abspath
    os.remove(file_path)

    ApiTestCase.objects.get(id=case_id).delete()

    api_test_case_list = ApiTestCase.objects.all()
    return render(request, 'apiTest.html', {"apiTestCaseList": api_test_case_list})


@login_required
def run_api_test(request, case_id):
    file_path = ApiTestCase.objects.get(id=case_id).case_abspath
    case_name = ApiTestCase.objects.get(id=case_id).name
    cd_templates = 'cd templates'
    command = cd_templates + '&& httprunner ' + file_path

    os.system(command)

    result_list = os.listdir('./templates/reports/%s' % case_name)

    api_test_case_list = ApiTestCase.objects.all()
    return render(request, 'apiTest.html', {"apiTestCaseList": api_test_case_list, "result_list": result_list})


@login_required
def show_api_result(request, case_id, result_file_name):
    case_name = ApiTestCase.objects.get(id=case_id).name
    return render(request, 'reports/%s/%s' % (case_name,result_file_name))


@login_required
def api_request(request):
    return render(request, 'request.html')


@login_required
def logout(request):
    auth.logout(request)  # 退出登录
    response = HttpResponseRedirect('/login/')
    return response
