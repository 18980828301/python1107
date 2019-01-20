from django.conf.urls import url

from goods.views import index, category

urlpatterns = [
    url(r'^index.html/$',index,name='首页'),
    url(r'^category.html/$',category,name='类别')
]
