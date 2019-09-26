from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.products_list, name='product_list'),
    url(r'^(?P<category_slug>[-\w]+)/$', views.products_list, name='product_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail')
]
