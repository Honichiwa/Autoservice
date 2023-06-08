from typing import Any, Dict, Optional
from datetime import date, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic
from . forms import OrderCommentForm, OrderForm, CarForm
from . models import Car, Order_info, Service, Order, OrderComment

def index(request):
    #susumuojam objektu reiksmes
    num_cars = Car.objects.all().count()
    num_orders_info = Order_info.objects.all().count()
    num_services = Service.objects.all().count()
    num_orders_done = Order.objects.filter(status__exact=2).count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    
    context = {
        'num_cars': num_cars,
        'num_orders_info': num_orders_info,
        'num_services': num_services,
        'num_orders_done':  num_orders_done,
        'num_visits': num_visits,
    }
    return render(request, 'car_service/index.html', context)



def car_list(request):
    qs = Car.objects
    query = request.GET.get('query')
    if query:
        qs = qs.filter(
            Q(client__first_name__icontains=query)
        )
    else:
        qs = qs.all()
    paginator = Paginator(qs, 3)
    car_list = paginator.get_page(request.GET.get('page'))
    return render (request, 'car_service/car_list.html', 
   { 'car_list': car_list})

def car_detail(request, pk: int):
    return render(request, 'car_service/car_detail.html',
    {'car': get_object_or_404(Car, pk=pk)})

class OrderListView(generic.ListView):
    model = Order
    # context_object_name = "orders"
    paginate_by = 5
    template_name = 'car_service/order_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            qs = qs.filter(
                Q(car__car_nr__icontains=query) |
                Q(car__client__first_name__icontains=query) |
                Q(car__car_model__make__istartswith=query)
            )
        return qs

class OrderDetailView(generic.edit.FormMixin,generic.DetailView):
    model = Order
    template_name = 'car_service/order_detail.html'
    form_class = OrderCommentForm

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        initial['order'] = self.get_object()
        initial['commenter'] = self.request.user
        return initial
    
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form: Any) -> HttpResponse:
        form.instance.order = self.get_object()
        form.instance.commenter = self.request.user
        form.save()
        messages.success(self.request, _('Comment Added!'))
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('order_detail', kwargs={'pk':self.get_object().pk})

class UserOrderList(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'car_service/user_order_list.html'
    paginate_by = 20

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(car__client=self.request.user)
        return qs
    
class UserCarList(LoginRequiredMixin, generic.ListView):
    model = Car
    template_name = 'car_service/user_car_list.html'
    paginate_by = 20

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(client=self.request.user)
        return qs

class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarForm
    template_name = 'car_service/car_form.html'
    success_url = reverse_lazy('user_car_list')

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        initial['client'] = self.request.user
        return initial
    
    def form_valid(self, form):
        form.instance.client = self.request.user
        messages.success(self.request, _('Car Added!'))
        return super().form_valid(form)
        

class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'car_service/order_form.html'
    success_url = reverse_lazy('user_order_list')

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        initial['cost'] = 1
        return initial
    
    def form_valid(self, form):
        form.instance.cost = 1
        messages.success(self.request, _('Order Created!'))
        return super().form_valid(form)


    
#     def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
#             context = super().get_context_data(**kwargs)
#             context['order'] = self.order
#             return context

    
