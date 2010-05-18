from django.contrib import admin
from accounts.models import Tester, Customer, JurCustomer, PhysCustomer

class TesterAdmin(admin.ModelAdmin):
    pass

class CustomerAdmin(admin.ModelAdmin):
    pass

class JurCustomerAdmin(admin.ModelAdmin):
    pass

class PhysCustomerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tester, TesterAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(JurCustomer, JurCustomerAdmin)
admin.site.register(PhysCustomer, PhysCustomerAdmin)

