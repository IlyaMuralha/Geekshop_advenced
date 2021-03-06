import random

from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page

from mainapp.models import Product, ProductCategory


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_ordered_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True,
                                              category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True,
                                      category__is_active=True).order_by('price')


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_ordered_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True,
                                              category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True,
                                      category__is_active=True).order_by('price')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_hot_product():
    product_ids = Product.objects.values_list('id', flat=True).all()
    random_id = random.choice(product_ids)
    return Product.objects.get(pk=random_id)


def same_products(hot_product):
    return Product.objects.filter(category=hot_product.category). \
               exclude(pk=hot_product.pk)[:3]


@cache_page(3600)
def index(request):
    context = {
        'page_title': '??????????????',
    }
    return render(request, 'mainapp/index.html', context)


def products(request):
    # basket = BasketItem.objects.fiter(user=request.user)
    # basket_price = sum(el.product.price for el in basket)
    hot_product = get_hot_product()
    context = {
        'page_title': '??????????????',
        'hot_product': hot_product,
        'same_products': same_products(hot_product),
        # 'categories': get_menu(),
        # # 'basket': basket,
    }
    return render(request, 'mainapp/products.html', context)


def category(request, pk):
    page_num = request.GET.get('page', 1)
    if pk == 0:
        category = {'pk': 0, 'name': '??????'}
        # products = Product.objects.all()
        products = get_products_ordered_by_price()
    else:
        # category = get_object_or_404(ProductCategory, pk=pk)
        category = get_category(pk)
        # products = category.product_set.all()
        products = get_products_in_category_ordered_by_price(pk)

    products_paginator = Paginator(products, 2)
    try:
        products = products_paginator.page(page_num)
    except PageNotAnInteger:
        products = products_paginator.page(1)
    except EmptyPage:
        products = products_paginator.page(products_paginator.num_pages)

    context = {
        'page_title': '???????????? ??????????????????',
        # 'categories': get_menu(),
        'category': category,
        'products': products,
    }
    return render(request, 'mainapp/category_products.html', context)


def product_page(request, pk):
    # product = get_object_or_404(Product, pk=pk)
    product = get_product(pk)
    context = {
        'page_title': '???????????????? ????????????????',
        'product': product,
        # 'categories': get_menu(),
    }
    return render(request, 'mainapp/product_page.html', context)


@cache_page(3600)
def contact(request):
    locations = [
        {'city': '????????????',
         'phone': '+7-888-444-7777',
         'email': 'info@geekshop.ru',
         'address': '?? ???????????????? ????????'},
        {'city': '??????????-??????????????????',
         'phone': '+7-888-333-9999',
         'email': 'info.spb@geekshop.ru',
         'address': '?? ???????????????? ??????'},
        {'city': '??????????????????',
         'phone': '+7-888-222-3333',
         'email': 'info.east@geekshop.ru',
         'address': '?? ???????????????? ????????????'},
    ]

    context = {
        'page_title': '????????????????',
        'locations': locations,
    }
    return render(request, 'mainapp/contact.html', context)
