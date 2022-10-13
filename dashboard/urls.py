from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('status-orderan', views.statusorderan, name='statusorderan'),
    path('tambah-orderan', views.tambahorderan, name='tambahorderan'),
    path('ubahstatus/<int:id>', views.ubah_status, name='ubah_status'),
    path('ubahworker/<int:id>', views.ubah_worker, name='ubah_worker'),
    path('penghasilan-worker', views.penghasilanworker, name='penghasilanworker'),
    path('account/', include('django.contrib.auth.urls'), name='login'),
    path('account/', include('django.contrib.auth.urls'), name='logout'),
    path('pembayaran-komisi', views.pembayarankomisi, name='pembayarankomisi'),
    path('atur-komisi', views.aturkomisi, name='aturkomisi'),
    path('tambah-produk-jasa', views.tambahprodukjasa, name='tambahprodukjasa'),
    path('hapusprodukjasa/<int:id>', views.hapusprodukjasa, name='hapusprodukjasa'),
    path('worker', views.listworker, name='worker'),
    path('editworker/<int:id>', views.editworker, name='editworker'),
    path('tambahworker', views.tambahworker, name='tambahworker'),
    path('hapusworker/<int:id>', views.hapusworker, name='hapusworker'),
    ]