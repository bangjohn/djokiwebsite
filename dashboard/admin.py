from django.contrib import admin
from .models import Order, Worker, ProdukJasa, TransaksiWithdraw, statusorderan
# Register your models here.
admin.site.register(Order)
admin.site.register(Worker)
admin.site.register(ProdukJasa)
admin.site.register(TransaksiWithdraw)
admin.site.register(statusorderan)

