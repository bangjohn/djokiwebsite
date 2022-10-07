from django.db import models
from django.utils import timezone

# Create your models here.
class Order(models.Model):
    tgl_order = models.DateTimeField(auto_now_add=True)
    nomor_hp_customer = models.CharField(max_length=15)
    nomor_id_ml = models.CharField(max_length=15)
    nomor_server_ml = models.CharField(max_length=15)
    rankawal = models.ForeignKey('rankML', on_delete=models.PROTECT, null=True, related_name='rankawal')
    rankakhir = models.ForeignKey('rankML', on_delete=models.PROTECT, null=True, related_name='rankakhir')
    nilai_transaksi = models.IntegerField()
    workerid = models.ForeignKey('Worker', on_delete=models.PROTECT, null=True, blank=True)
    produkjasa = models.ForeignKey('ProdukJasa', on_delete=models.PROTECT, null=True, blank=True)
    status = models.ForeignKey('statusorderan', on_delete=models.PROTECT, null=True, blank=True)
    def __str__(self):
        return f'{self.nomor_hp_customer} {self.nomor_id_ml} {self.nomor_server_ml}'

class Worker(models.Model):
    nama = models.CharField(max_length=15)
    nomor_hp = models.CharField(max_length=15)
    pendapatankomisi = models.IntegerField()
    def __str__(self):
        return 'Worker %s' % (self.nama)

class ProdukJasa(models.Model):
    nama = models.CharField(max_length=15, blank=True, null=True)
    komisi = models.IntegerField()
    def __str__(self):
        return '%s' % (self.nama)

class rankML(models.Model):
    rank1 = models.CharField(max_length=50, blank=True, null=True)
    rank2 = models.CharField(max_length=50, blank=True, null=True)
    rank3 = models.CharField(max_length=50, blank=True, null=True)
    harga = models.IntegerField()
    urutan = models.IntegerField()
    def __str__(self):
        return 'Rank %s' % (self.rank3)

class TransaksiWithdraw(models.Model):
    tgl_transaksi = models.DateTimeField(auto_now_add=True)
    workerid = models.ForeignKey('Worker', on_delete=models.CASCADE)
    nilai_transaksi = models.IntegerField()
    def __str__(self):
        return 'TransaksiWithdraw %s' % (self.workerid)

class statusorderan(models.Model):
    keterangan = models.CharField(max_length=50)
    def __str__(self):
        return '%s' % (self.keterangan)

    # class for komisi pendapatanworker
class PendapatanWorker(models.Model):
    workerid = models.ForeignKey('Worker', on_delete=models.PROTECT, null=True, blank=True)
    orderanid = models.ForeignKey('Order', on_delete=models.PROTECT, null=True, blank=True)
    tgl_transaksi = models.DateTimeField(auto_now_add=True)
    nilai_komisi = models.IntegerField()
    def __str__(self):
        return 'PendapatanWorker %s' % (self.nilai_komisi)