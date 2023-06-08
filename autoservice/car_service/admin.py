from django.contrib import admin
from .models import Car, Carmodel, Order_info, Order, Service, OrderComment
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class CarModelAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year')

class Order_infoInline(admin.TabularInline):
    model = Order_info
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('car', 'date', 'status', 'due_back', 'is_overdue')
    inlines = [Order_infoInline]
    # fieldsets = (
    #     (_('Status'), {'fields': ('status',)}),
    # )
    

class CarAdmin(admin.ModelAdmin):
    list_display = ('client', 'client_name', 'car_model', 'car_nr', 'vin')
    list_filter = ('client__first_name', 'car_model')
    search_fields = ('car_nr', 'vin')
    def client_name(self, obj):
        if obj.client == None:
                return obj.client
        else:
            return f'{obj.client.first_name} {obj.client.last_name}'


class Order_infoAdmin(admin.ModelAdmin):
    list_display = ('service', 'price')

class OrderCommentAdmin(admin.ModelAdmin):
     list_display = ('commented_at', 'order', 'commenter', 'content')

admin.site.register(Car, CarAdmin)
admin.site.register(Carmodel, CarModelAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Order_info, Order_infoAdmin)
admin.site.register(Service)
admin.site.register(OrderComment, OrderCommentAdmin)
admin.site.site_header = 'AutoTadas'
admin.site.site_title = 'AutoTadas admin'
admin.site.index_title = ''

