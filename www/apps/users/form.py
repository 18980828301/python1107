from django import forms
from django.core.validators import RegexValidator

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
        else:
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