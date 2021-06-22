from django.urls import path

import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    path('', basketapp.index, name='index'),
    path('add/<int:product_pk>/', basketapp.add, name='add'),
    path('remove/<int:basket_item_pk>/', basketapp.remove, name='remove'),
    # "/basket/update/" + basketItemPk + "/" + qty + "/"
    path('update/<int:basket_item_pk>/<int:qty>/', basketapp.update),
]
