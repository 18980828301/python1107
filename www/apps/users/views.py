from django.http import HttpResponse
from django.shortcuts import render,redirect

# Create your views here.
from django.views import View


#登录
from users import set_password
from users.form import RegisterModelForm, LoginModelForm
from users.models import Users


class LoginView(View):
    #展示登录页面
    def get(self,request):
        return render(request,'users/login.html')
    def post(self,request):
        #接受数据
        data=request.POST
        form=LoginModelForm(data)
        #判断是否合法
        if form.is_valid():
            #验证成功
            return redirect('users:个人中心')
        else:
            return render(request,'users/login.html',context={'form':form})

#注册
class RegisterView(View):
    #get请求 展示登录表单
    def get(self,request):
        return render(request,'users/reg.html')
    def post(self,request):
        #post请求 接受参数
        data=request.POST
        #表单验证
        form=RegisterModelForm(data)
        #表单验证成功
        if form.is_valid():
        #操作数据库
            cleande_data=form.cleaned_data
            user = Users()
            user.num = cleande_data.get('num')
            user.password = set_password(cleande_data.get('password'))
            user.save()
            return redirect('users:登录')
        else:
            return render(request,'users/reg.html',context={'form':form})
class MemberView(View):
    def get(self,request):
        return render(request,'users/member.html')




