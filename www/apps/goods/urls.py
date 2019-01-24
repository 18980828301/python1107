from django.conf.urls import url

from goods.views import  CategoryView, detail, TidingsView, CityView

urlpatterns = [
    url(r'^category/$',CategoryView.as_view(),name='超市'),
    url(r'^detail/(?P<id>\d+)/$', detail, name="详情"),
    url(r'^tidings/$',TidingsView.as_view(),name='消息中心'),
    url(r'^city/$',CityView.as_view(),name='城市'),
]
