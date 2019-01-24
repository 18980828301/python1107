from django.contrib import admin

# Register your models here.
from goods.models import GoodsClassModel, GoodsSPUModel, GoodsUnitModel, GoodsskuClassModel, GoodsAlbumModel, \
    BannerModel, IndexActModel, HomeActarea

admin.site.register(GoodsClassModel)
admin.site.register(GoodsSPUModel)
admin.site.register(GoodsUnitModel)
admin.site.register(GoodsskuClassModel)
admin.site.register(GoodsAlbumModel)
admin.site.register(BannerModel)
admin.site.register(IndexActModel)
admin.site.register(HomeActarea)