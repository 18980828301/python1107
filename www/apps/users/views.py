import re
import random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django_redis import get_redis_connection
# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

# 登录
from db.base_view import VerifyLoginView
from users import set_password
from users.form import RegisterModelForm, LoginModelForm, PasswordModelForm, ForgetpasswordModelForm
from users.helper import check_login, login
from users.models import Users


# 登录
class LoginView(View):
    # 展示登录页面
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        # 接受数据
        data = request.POST
        form = LoginModelForm(data)
        # 判断是否合法
        if form.is_valid():
            # 验证成功
            # 保存登录标识到session中, 单独创建一个方法保存, 更新个人资料
            user = form.cleaned_data['user']
            login(request, user)
            return redirect('users:个人中心')
        else:
            return render(request, 'users/login.html', context={'form': form})


# 注册
class RegisterView(View):
    # get请求 展示登录表单
    def get(self, request):
        return render(request, 'users/reg.html')

    def post(self, request):
        # post请求 接受参数
        data = request.POST
        # 表单验证
        form = RegisterModelForm(data)
        # 表单验证成功
        if form.is_valid():
            # 操作数据库
            cleande_data = form.cleaned_data
            user = Users()
            user.num = cleande_data.get('num')
            user.password = set_password(cleande_data.get('password'))
            user.save()
            return redirect('users:登录')
        else:
            return render(request, 'users/reg.html', context={'form': form})


# 发送短信
class SendMsg(View):
    def get(self, request):
        pass

    def post(self, request):
        # 接受参数
        num = request.POST.get('num', '')
        rs = re.search('^1[3-9]\d{9}$', num)
        # 判断电话号码的合法性
        if rs is None:
            return JsonResponse({'error': 1, 'errormsg': '电话号码错误'})


        # 处理数据
        # 模拟,最后接入运营商
        # """
        #     1. 生成随机验证码
        #     2. 保存验证码 保存到redis中, 存取速度快,并且可以方便的设置有效时间
        #     3. 接入运营商
        # """
        # >>>1. 生成随机验证码字符串
        random_code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        print("=============随机验证码为==={}==============".format(random_code))

        # >>>2. 保存验证码到redis中
        # 获取连接
        r = get_redis_connection()
        # 保存手机号码对应的验证码
        r.set(num, random_code)
        r.expire(num, 60)  # 设置60秒后过期

        # 首先获取当前手机号码的发送次数
        key_times = "{}_times".format(num)
        now_times = r.get(key_times)  # 从redis获取的二进制,需要转换
        # print(int(now_times))
        if now_times is None or int(now_times) < 5:
            # 保存手机发送验证码的次数, 不能超过5次
            r.incr(key_times)
            # 设置一个过期时间
            r.expire(key_times, 3600)  # 一个小时后再发送
        else:
            # 返回,告知用户发送次数过多
            return JsonResponse({"error": 1, "errmsg": "发送次数过多"})

        return JsonResponse({'error': 0})


# 个人中心
class MemberView(VerifyLoginView):
    def get(self, request):
        return render(request, 'users/member.html')

    def post(self, request):
        pass


# 安全中心
class SaftyView(VerifyLoginView):
    def get(self, request):
        return render(request, 'users/saftystep.html')

    def post(self, request):
        pass


# 绑定手机号
class BoundphoneView(VerifyLoginView):
    def get(self, request):
        return render(request, 'users/boundphone.html')

    def post(self, request):
        pass


# 修改密码
class PasswordView(VerifyLoginView):
    def get(self, request):
        return render(request, 'users/password.html')

    def post(self, request):
        # return HttpResponse('ok')
        # 接收数据
        data = request.POST
        form = PasswordModelForm(data)
        # 验证表单成功
        if form.is_valid():
            cleaned_data = form.cleaned_data
            # 操作数据库
            password = cleaned_data.get('password')
            newpassword = cleaned_data.get('newpassword')
            # 更新到数据库
            Users.objects.filter(password=password).update(password=set_password(newpassword))
            return redirect('users:登录')
        else:
            return render(request, 'users/password.html', context={'form': form})


# 忘记密码
class ForgetpasswordView(VerifyLoginView):
    def get(self, request):
        return render(request, 'users/forgetpassword.html')

    def post(self, request):
        # 接收数据
        data = request.POST
        form = ForgetpasswordModelForm(data)
        # 验证表单成功
        if form.is_valid():
            cleaned_data = form.cleaned_data
            # 操作数据库
            num = cleaned_data.get('num')
            password = cleaned_data.get('password')
            newpassword = cleaned_data.get('newpassword')
            # 更新到数据库
            Users.objects.filter(num=num).update(password=set_password(newpassword))
            return redirect('users:登录')
        else:
            return render(request, 'users/forgetpassword.html', context={'form': form})


# 个人资料
class InfoView(VerifyLoginView):
    def get(self, request):
        id = request.session.get('ID')
        num = request.session.get('num')
        user = Users.objects.get(num=num)
        return render(request, 'users/infor.html', context={'user': user})

    def post(self, request):
        # 接收参数
        data = request.POST
        head = request.FILES.get('head')
        id = request.session.get('ID')
        num = request.session.get('num')
        # 验证数据合法性
        nickname = data.get('nickname')
        school = data.get('school')
        hometown = data.get('hometown')
        birthday = data.get('birthday')
        location = data.get('location')
        gender = int(data.get('gender'))
        user = Users.objects.get(pk=id)
        # 把接收到的参数更新到数据库
        Users.objects.filter(id=id).update(nickname=nickname, school=school, hometown=hometown, birthday=birthday,location=location, gender=gender)
        if head is not None:
            user.head = head
        user.save()
        # 同时修改session
        login(request, user)
        return redirect('users:个人中心')
