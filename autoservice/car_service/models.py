from django.contrib.auth import get_user_model
from datetime import date
from typing import Iterable, Optional
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from tinymce.models import HTMLField

User = get_user_model()

class Carmodel(models.Model):

    make = models.CharField(_("make"), max_length=100)
    model = models.CharField(_("model"), max_length=100)
    year = models.IntegerField(_("year"))

    class Meta:
        ordering = ['make', 'model']
        verbose_name = _("carmodel")
        verbose_name_plural = _("carmodels")

    def __str__(self):
        return f'{self.make} {self.model} {self.year}'

    def get_absolute_url(self):
        return reverse("carmodel_detail", kwargs={"pk": self.pk})

class Car(models.Model):

    car_nr = models.CharField(_("car nr"), max_length=20)
    vin = models.CharField(_("vin"), max_length=50)
    car_model = models.ForeignKey(
        Carmodel, 
        verbose_name=_("carmodel"), 
        on_delete=models.CASCADE,
        related_name='cars'
        )
    client = models.ForeignKey(
        User, 
        verbose_name=_("client"),
        on_delete=models.CASCADE,
        related_name='cars',
        null=True, blank=True,
        db_index=True,
        )
    cover = models.ImageField(
        _("cover"), 
        upload_to='car_service/car_covers',
        blank=True,
        null=True
    )
    description = models.TextField(_("description"), max_length=8000, blank=True, null=True)

    class Meta:
        ordering = ['car_nr', 'car_model']
        verbose_name = _("car")
        verbose_name_plural = _("cars")

    def __str__(self):
        return f'{self.car_nr} {self.car_model}'

    def get_absolute_url(self):
        return reverse("car_detail", kwargs={"pk": self.pk})
    
class Order(models.Model):

    date= models.DateField(_("date"), auto_now=False, auto_now_add=False)
    cost = models.IntegerField(_("cost"),null=True)
    car = models.ForeignKey(
        Car, 
        verbose_name=_("car"),
        on_delete=models.CASCADE, 
        related_name='orders')
    due_back = models.DateField(_("due back"), null=True, blank=True, db_index=True)
    summary = HTMLField(_("order_summary"), max_length=8000, blank=True, null=True)

    STATUS_CHOICES = (
        (0, _('Waiting')),
        (1, _('In progress')),
        (2, _('Finished')),
        (3, _('Ready for pick up')),
        (7, _('Not fixable'))
    )

    status = models.PositiveBigIntegerField(
        _("status"),
        choices=STATUS_CHOICES,
        default=0,
        db_index=True)
    
    class Meta:
        ordering = ['car', 'date', 'cost']
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    def __str__(self):
        return f'{self.car} {self.date}'

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"pk": self.pk})
   
    def total_sum(self):
        order_info = Order_info.objects.filter(order_id=self.id)
        cost = 0
        for order in order_info:
            cost += order.quantity * order.price
        return cost
    
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False


class Service(models.Model):

    name = models.CharField(_("name"), max_length=50)
    price = models.IntegerField(_("price"))

    class Meta:
        ordering = ['name', 'price']
        verbose_name = _("service")
        verbose_name_plural = _("services")

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("service_detail", kwargs={"pk": self.pk})
    

class Order_info(models.Model):

    service = models.ForeignKey(
        Service, 
        verbose_name=_("services"),
        on_delete=models.CASCADE, 
        related_name="order_infos")
    order = models.ForeignKey(
        Order, 
        verbose_name=_("orders"), 
        on_delete=models.CASCADE,
        related_name='order_infos')
    quantity = models.IntegerField(_("quantity"))
    price = models.IntegerField(_("price"), default=0)

    class Meta:
        ordering = ['service', 'quantity', 'price']
        verbose_name = _("order_info")
        verbose_name_plural = _("order_infos")

    def __str__(self):
        return f'{self.service} {self.order} {self.quantity} {self.price}'

    def get_absolute_url(self):
        return reverse("order_info_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if self.price == 0:
            self.price = self.service.price
        super().save(*args, **kwargs)

class OrderComment(models.Model):

    order = models.ForeignKey(
        Order,
        verbose_name=_("order"),
        on_delete=models.CASCADE,
        related_name='comments',
    )
    commenter = models.ForeignKey(User, 
        verbose_name=_("commenter"), 
        on_delete=models.SET_NULL,
        related_name='order_comments',
        null=True, blank=True
    )
    commented_at = models.DateTimeField(_("Commented"),auto_now_add=True)
    content = models.TextField(_("content"), max_length=4000)

    class Meta:
        ordering = ['commented_at']
        verbose_name = _("order comment")
        verbose_name_plural = _("order comments")

    def __str__(self):
        return f'{self.commented_at}: {self.commenter}'

    def get_absolute_url(self):
        return reverse("ordercomment_detail", kwargs={"pk": self.pk})
