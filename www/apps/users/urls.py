from django.conf.urls import url

from users.views import LoginView, RegisterView, MemberView, SaftyView, PasswordView, ForgetpasswordView, InfoView, \
    BoundphoneView, SendMsg

urlpatterns = [
    url(r'^login/$',LoginView.as_view(),name='登录' ),
    url(r'^register/$',RegisterView.as_view(),name='注册' ),
    url(r'^member/$',MemberView.as_view(),name='个人中心' ),
    url(r'^safty/$',SaftyView.as_view(),name='安全设置' ),
    url(r'^password/$',PasswordView.as_view(),name='修改密码' ),
    url(r'^forgetpassword/$',ForgetpasswordView.as_view(),name='忘记密码' ),
    url(r'^info/$',InfoView.as_view(),name='个人资料' ),
    url(r'^boundphone/$',BoundphoneView.as_view(),name='绑定手机号' ),
    url(r'^sendmsg/$',SendMsg.as_view(),name='发送短信验证码' ),
]
