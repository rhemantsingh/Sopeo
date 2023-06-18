from django.contrib import admin

# Register your models here.
from .models import Inventory, Orders, Transaction

admin.site.register(Inventory)
admin.site.register(Orders)
admin.site.register(Transaction)
