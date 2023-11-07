from django.contrib import admin

from .models import Customer, PaymentMethod, PaymentIntent


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['stripe_id', 'name', 'email']
    search_fields = ['name', 'email', 'stripe_id']
    raw_id_fields = ['user']


class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['stripe_id', 'last4', 'customer', 'brand', 'country']
    search_fields = ['customer__name', 'customer__email', 'stripe_id', 'last4']
    raw_id_fields = ['user', 'customer']


class PaymentIntentAdmin(admin.ModelAdmin):
    list_display = ['stripe_id', 'status', 'amount']
    search_fields = ['stripe_id', 'payment_method__customer__email']
    raw_id_fields = ['customer', 'payment_method']


admin.site.register(Customer, CustomerAdmin)
admin.site.register(PaymentMethod, PaymentMethodAdmin)
admin.site.register(PaymentIntent, PaymentIntentAdmin)
