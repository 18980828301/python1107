from django.shortcuts import render, redirect

# Create your views here.
from db.base_view import VerifyLoginView
from goods.models import GoodsSPUModel, GoodsskuClassModel, GoodsClassModel


class IndexView(VerifyLoginView):
    def get(self,request):
        return render(request,'goods/index.html')
    def post(self,request):
        pass
class CategoryView(VerifyLoginView):
    def get(self,request):
        # 查询所有的分类
        goods = GoodsClassModel.objects.filter(is_delete=False)
        # 查询所有的商品
        goods_skus = GoodsskuClassModel.objects.filter(is_delete=False)
        context={
            'goods':goods,
            'goods_skus':goods_skus,
        }
        return render(request,'goods/category.html',context=context)
    def post(self,request):
        pass
def detail(request,id):
    try:
        goods = GoodsskuClassModel.objects.get(pk=id)
    except GoodsskuClassModel.DoesNotExist:
        return redirect("goods:首页")
    context={
        'goods':goods
        }
    return render(request,'goods/detail.html',context=context)
class TidingsView(VerifyLoginView):
    def get(self,request):
        return render(request,'goods/tidings.html')
    def post(self,request):
        pass
class CityView(VerifyLoginView):
    def get(self,request):
        return render(request,'goods/city.html')
    def post(self,request):
        pass