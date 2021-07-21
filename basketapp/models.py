from django.contrib.auth import get_user_model
from django.db import models
from django.utils.functional import cached_property

from mainapp.models import Product


# class BasketQuerySet(models.QuerySet):
#
#     def delete(self):
#         for item in self:
#             item.product.quantity += item.quantity
#             item.product.save()
#             super().delete()


class BasketItem(models.Model):
    # objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('количество', default=0)
    add_dt = models.DateTimeField('время', auto_now_add=True)
    update_dt = models.DateTimeField('время', auto_now=True)

    # @cached_property
    # def get_items_cached(self):
    #     return self.user.basket.select_related()

    # def get_total_quantity(self):
    #     _items = self.get_items_cached
    #     return sum(list(map(lambda x: x.quantity, _items)))
    #
    # def get_total_cost(self):
    #     _items = self.get_items_cached
    #     return sum(list(map(lambda x: x.product_cost, _items)))

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_item(pk):
        return BasketItem.objects.get(pk=pk)

    # def delete(self, *args, **kwargs):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super().delete(*args, **kwargs)
    #
    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         self.product.quantity -= self.quantity - self.__class__.objects.get(pk=self.pk).quantity
    #     else:
    #         self.product.quantity -= self.quantity
    #     self.product.save()
    #     super(self).save(*args, **kwargs)
