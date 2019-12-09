from django.urls import re_path
from . import views

app_name = 'shop'

urlpatterns = [
	re_path('^$',views.product_list,name='product_list'),
	re_path('^(?P<category_slug>[-\w]+)/$',views.product_list,name='product_list_category'),
	re_path('^(?P<id>\d+)/(?P<slug>[-\w]+)/$',views.product_detail,name='product_detail'),
]
