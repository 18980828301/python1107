from datetime import date

from django import forms
from django.core.validators import RegexValidator
from django_redis import get_redis_connection

from users import set_password
from users.models import Users



class RegisterModelForm(forms.ModelForm):
    """注册表单模型类"""

    # 单独定义一个字段
    password = forms.CharField(max_length=16,
                               min_length=8,
                               error_messages={
                                   'required': '必须填写密码',
                                   'min_length': '密码最小长度必须为8位',
                                   'max_length': '密码最大长度不能超过16位',
                               })
    repassword = forms.CharField(max_length=16,
                                 min_length=8,
                                 error_messages={
                                     'required': '必须填写确认密码',
                                     'min_length': '密码最小长度必须为8位',
                                     'max_length': '密码最大长度不能超过16位',
                                 })
    # 验证码
    captcha = forms.CharField(max_length=6,
                              error_messages={
                                  'required': "验证码必须填写"
                              })

    agree = forms.BooleanField(error_messages={
        'required': '必须同意用户协议'
    })

    class Meta:
        model = Users
        fields = ['num']

        error_messages = {
            "num":{
                'required': '手机号码必须填写',
                'max_length': '手机号码长度必须为11位',
            }
        }

    def clean_num(self):#验证手机号码是否存在
        num = self.cleaned_data.get('num')
        flag = Users.objects.filter(num=num).exists()
        if flag:
            # 存在 错误
            raise forms.ValidationError("手机号码已经被注册")
        else:
            return num

    def clean(self):
        # 判断两次密码是否一致
        pwd = self.cleaned_data.get('password')
        repwd = self.cleaned_data.get('repassword')
        if pwd and repwd and pwd != repwd:
            raise forms.ValidationError({'repassword': "两次密码不一致"})


        # 综合校验
        # 验证 用户传入的验证码和redis中的是否一样
        # 用户传入的
        try:
            captcha = self.cleaned_data.get('captcha')
            num = self.cleaned_data.get('num','')
            # 获取redis中的
            r = get_redis_connection()
            random_code = r.get(num)  # 二进制, 转码
            random_code = random_code.decode('utf-8')
            # 比对
            if captcha and captcha != random_code:
                raise forms.ValidationError({"captcha": "验证码输入错误!"})
        except:
            raise forms.ValidationError({"captcha": "验证码输入错误!"})
        return self.cleaned_data


class LoginModelForm(forms.ModelForm):
    """注册表单模型类"""

    # 单独定义一个字段
    password = forms.CharField(max_length=16,
                               min_length=8,
                               error_messages={
                                   'required': '必须填写密码',
                                   'min_length': '密码最小长度必须为8位',
                                   'max_length': '密码最大长度不能超过16位',
                               })

    class Meta:
        model = Users
        fields = ['num']

        error_messages = {
            "num": {
                'required': '手机号码必须填写',
                'max_length': '手机号码长度必须为11位',
            }
        }

    def clean(self):
        # 验证用户名
        num = self.cleaned_data.get('num')
        # 查询数据库
        try:
            user = Users.objects.get(num=num)
        except Users.DoesNotExist:
            raise forms.ValidationError({'num': '手机号码错误'})

        # 验证密码
        password = self.cleaned_data.get('password','')
        if user.password != set_password(password):
            raise forms.ValidationError({'password': '密码错误'})

        # 返回所有清洗后的数据
        self.cleaned_data['user'] = user
        return self.cleaned_data

class PasswordModelForm(forms.ModelForm):
    newpassword = forms.CharField(max_length=16,
                               min_length=8,
                               error_messages={
                                   'required': '必须填写新密码',
                                   'min_length': '密码最小长度必须为8位',
                                   'max_length': '密码最大长度不能超过16位',
                               })
    renewpassword = forms.CharField(max_length=16,
                                  min_length=8,
                                  error_messages={
                                      'required': '必须填写确认密码',
                                      'min_length': '密码最小长度必须为8位',
                                      'max_length': '密码最大长度不能超过16位',
                                  })
    class Meta:
        model = Users
        fields = ['password','newpassword','renewpassword']
        error_messages={
            'password':{
                'required': '旧密码必须填写',
            }
        }
    def clean_password(self):
        #验证密码是否存在
        password=set_password(self.cleaned_data.get('password'))
        flag=Users.objects.filter(password=password).exists()
        #密码存在
        if flag:
            return password
        #密码不存在
        else:
            raise forms.ValidationError("旧密码错误")

    def clean(self):
        # 判断两次密码是否一致
        newpassword = self.cleaned_data.get('newpassword')
        renewpassword = self.cleaned_data.get('renewpassword')
        if renewpassword and newpassword and renewpassword != newpassword:
            raise forms.ValidationError({'renewpassword': "两次密码不一致"})
        else:
            return self.cleaned_data

class ForgetpasswordModelForm(forms.ModelForm):
    newpassword = forms.CharField(max_length=16,
                               min_length=8,
                               error_messages={
                                   'required': '必须填写新密码',
                                   'min_length': '密码最小长度必须为8位',
                                   'max_length': '密码最大长度不能超过16位',
                               })
    renewpassword = forms.CharField(max_length=16,
                                  min_length=8,
                                  error_messages={
                                      'required': '必须填写确认密码',
                                      'min_length': '密码最小长度必须为8位',
                                      'max_length': '密码最大长度不能超过16位',
                                  })
    class Meta:
        model = Users
        fields = ['num','newpassword','renewpassword']
        error_messages={
            'num':{
                'required': '电话号码必须填写',
            }
        }
    def clean_num(self):
        #验证密码是否存在
        num=self.cleaned_data.get('num')
        flag=Users.objects.filter(num=num).exists()
        #密码存在
        if flag:
            return num
        #密码不存在
        else:
            raise forms.ValidationError("手机号码错误")
    def clean(self):
        # 判断两次密码是否一致
        newpassword = self.cleaned_data.get('newpassword')
        renewpassword = self.cleaned_data.get('renewpassword')
        if renewpassword and newpassword and renewpassword != newpassword:
            raise forms.ValidationError({'renewpassword': "两次密码不一致"})
        else:
            return self.cleaned_data

# class InfoViewModelForm(forms.ModelForm):
#     class Meta:
#         model = Users
#         fields = ['num','birthday']
#         error_messages={
#             'num':{
#                 'required': '电话号码必须填写',
#             },
#         }
#     def clean_birthday(self):
#         birthday = self.cleaned_data.get('birthday')
#         if birthday > date.today():
#             raise forms.ValidationError("日期错误")
#         else:
#             return birthday
