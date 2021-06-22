from django.urls import path, re_path

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.index, name='index'),
    path('products/', mainapp.products, name='products'),
    path('contact/', mainapp.contact, name='contact'),

    path('category/<int:pk>/', mainapp.category, name='category'),
    # re_path('category/(?P<pk>\d+)/$', mainapp.category, name='category'),
    path('product/<int:pk>/', mainapp.product_page, name='product_page'),

]
