from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Voucher)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Ordered)
admin.site.register(OrderItem)
admin.site.register(new)
admin.site.register(Comment)
admin.site.register(Liked)
admin.site.register(StatusOrder)