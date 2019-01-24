from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from db.base_model import BaseModel


# 1.商品分类表
class GoodsClassModel(BaseModel):
    classname = models.CharField(max_length=6, verbose_name='分类名')
    classintro = models.TextField(max_length=40, verbose_name='分类简介')

    class Meta:
        db_table = 'GoodsClassModel'
        verbose_name = '商品分类信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.classname


# 2.商品SPU表
class GoodsSPUModel(BaseModel):
    SPUname = models.CharField(max_length=50, verbose_name='spu名称')
    SPUdetails = RichTextUploadingField(verbose_name='spu详情')

    class Meta:
        db_table = 'GoodsSPUModel'
        verbose_name = '商品SPU表'
        verbose_name_plural = verbose_name  # 复数名

    def __str__(self):
        return self.SPUname


# 3.商品单位表
class GoodsUnitModel(BaseModel):
    unitname = models.CharField(max_length=10, verbose_name='单位名')

    class Meta:
        db_table = 'GoodsUnitModel'
        verbose_name = '商品单位表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.unitname


# 4.商品sku表
class GoodsskuClassModel(BaseModel):
    goodsname = models.CharField(max_length=10, verbose_name='商品名')
    goodsintro = models.CharField(max_length=30, verbose_name='商品简介')
    goodsprice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    stock = models.SmallIntegerField(verbose_name='库存')
    goodslogo = models.ImageField(upload_to='goodslogo/%y%m/%d', verbose_name='商品logo')
    choic = (
        (False, '未上架'),
        (True, '已上架'),
    )
    shelves = models.BooleanField(choices=choic, verbose_name='是否上架')
    # 商品分类ID  外键  GoodsClassModel
    goodsclass_id = models.ForeignKey(to='GoodsClassModel', verbose_name='商品分类ID')
    # 商品spu_id   外键  GoodsSPUModel
    goodsspu_id = models.ForeignKey(to='GoodsSPUModel', verbose_name='商品spu_id')
    # 单位 外键   UnitModel
    unit = models.ForeignKey(to='GoodsUnitModel', verbose_name='单位')

    class Meta:
        db_table = 'GoodsskuClassModel'
        verbose_name = '商品SKU表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goodsname


# 5.商品相册表
class GoodsAlbumModel(BaseModel):
    photourl = models.ImageField(upload_to='goods/%y%m/%d', verbose_name='图片地址')
    goodsSKUID = models.ForeignKey(to='GoodsskuClassModel', verbose_name='商品SKUID')

    class Meta:
        db_table = 'GoodsAlbumModel'
        verbose_name = '商品相册表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '商品相册:{}'.format(self.photourl.name)


# 6.首页轮播商品表
class BannerModel(BaseModel):
    goodsName = models.CharField(max_length=30, verbose_name='商品名称')
    # 商品SKUID  外键
    goodsSKU = models.ForeignKey(to=GoodsskuClassModel, verbose_name='商品SKUID')
    # 图片地址
    photourl = models.ImageField(upload_to='banner/%y%m/%d', verbose_name='商品相册')
    # 排序（order）
    bannerOrder = models.SmallIntegerField()

    class Meta:
        db_table = 'BannerModel'
        verbose_name = '首页轮播商品表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goodsName


# 7 首页活动表
class IndexActModel(models.Model):
    name = models.CharField(max_length=30, verbose_name='名称')
    photourl = models.ImageField(upload_to='activity/%y%m/%d', verbose_name='活动图片')
    # url地址
    url = models.CharField(max_length=100, verbose_name='url地址')

    class Meta:
        db_table = 'IndexActModel'
        verbose_name = '首页活动表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 8首页活动专区
class HomeActarea(BaseModel):
    name = models.CharField(max_length=30, verbose_name='名称')
    desc = models.TextField(max_length=200, verbose_name='描述')
    order = models.SmallIntegerField()
    skuid = models.ManyToManyField(to=GoodsskuClassModel, verbose_name='和商品sku多对多')
    choic = (
        (False, '未上架'),
        (True, '已上架'),
    )
    shelves = models.BooleanField(choices=choic, verbose_name='是否上架')

    class Meta:
        db_table = 'HomeActarea'
        verbose_name = '首页活动专区'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
