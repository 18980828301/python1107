from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator


# Create your models here.
class Users(models.Model):
    num = models.CharField(max_length=11,
                                validators=[
                                    MinLengthValidator(11, '手机号码必须为11位'),
                                    RegexValidator(r'^1[3-9]\d{9}$', "手机号码格式错误!")
                                ])
    gender_choices = (
        (1,'男'),
        (2,'女'))
    password = models.CharField(max_length=32)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateField(auto_now_add=True) #添加时间
    update_time = models.DateField(auto_now=True) #修改时间
    nickname=models.CharField(max_length=200,null=True,blank=True)  #昵称
    birthday=models.DateField(null=True,blank=True)
    gender=models.SmallIntegerField(choices=gender_choices,default=1)
    school=models.CharField(null=True,max_length=200,blank=True)
    location=models.CharField(null=True,max_length=200,blank=True)
    hometown=models.CharField(null=True,max_length=200,blank=True)
    def __str__(self):
        return self.num

    class Meta:
        db_table = "users"