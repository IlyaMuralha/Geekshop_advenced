from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from basketapp.models import BasketItem
from geekshop.settings import LOGIN_URL


@login_required
def index(request):
    basket = request.user.basket.all()
    context = {
        'page_title': 'корзина',
        'basket': basket,
    }
    return render(request, 'basketapp/index.html', context)


@login_required
def add(request, product_pk):
    if LOGIN_URL in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(
            reverse('main:product_page',
                    kwargs={'pk': product_pk}))

    basket_item, _ = BasketItem.objects.get_or_create(
        user=request.user,
        product_id=product_pk
    )
    basket_item.quantity = F('quantity') + 1
    # # Используем F вместо python обращения
    # basket_item.quantity += 1
    basket_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove(request, basket_item_pk):
    item = get_object_or_404(BasketItem, pk=basket_item_pk)
    item.delete()
    return HttpResponseRedirect(reverse('basket:index'))


def update(request, basket_item_pk, quantity):
    if request.is_ajax():
        item = BasketItem.objects.filter(pk=basket_item_pk).first()
        if not item:
            return JsonResponse({'status': False})
        if quantity == 0:
            item.delete()
        else:
            item.quantity = quantity
            item.save()
        basket_summary_html = render_to_string(
            'basketapp/includes/basket_summary.html',
            request=request
        )
        print(basket_summary_html)
        return JsonResponse({'status': True,
                             'basket_summary': basket_summary_html,
                             'quantity': quantity})
