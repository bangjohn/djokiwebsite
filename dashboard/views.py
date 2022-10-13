from django.db.models import *
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Order, Worker, ProdukJasa, statusorderan, PendapatanWorker, TransaksiWithdraw
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
import json
import requests
from .forms import *

# Create your views here.

def login_masuk(request):
    return render(request, 'dashboard/../templates/registration/login.html')
@login_required(login_url='login')
def index(request):
    # sum nilai transaksi from dashboard_order tables all row
    sumnilai = Order.objects.all().aggregate(Sum('nilai_transaksi'))
    # count all row from dashboard_order tables
    countorder = Order.objects.all().count()
    # count all row from dashboard_order tables where status = 1
    countorderpending = Order.objects.filter(status=1).count()
    # count all row from dashboard_order tables where status = 2
    countorderproses = Order.objects.filter(status=2).count()
    # count all row from dashboard_order tables where status = 3
    countorderselesai = Order.objects.filter(status=3).count()
    return render(request, 'dashboard/index.html', {
        'sumnilai': sumnilai,
        'countorder': countorder,
        'countorderpending': countorderpending,
        'countorderproses': countorderproses,
        'countorderselesai': countorderselesai,
    })

@login_required(login_url='login')
def statusorderan(request):
    # inner join worker and order where order.workerid = worker.id
    order = Order.objects.select_related('workerid', 'produkjasa', 'status').all().order_by('-tgl_order')
    nomorid = Order.objects.values_list('nomor_id_ml', flat=True).distinct().order_by('-tgl_order')
    return render(request, 'dashboard/status-orderan.html', {
        'orderan': order,
        'formubahstatus': formubahstatus(),
        'formubahworker': formubahworker(),
    })

@login_required(login_url='login')
def ubah_status(request, id):
    if request.method == "POST":
        orderid = Order.objects.get(id=id)
        form = formubahstatus(request.POST, instance=orderid)
        if form.is_valid():
            new_status = form.cleaned_data['status']

            nilai_transaksi = Order.objects.get(id=id).nilai_transaksi
            if str(new_status) == 'Selesai':
                workernya = Order.objects.select_related('workerid').get(id=id).workerid_id
                orderannya = Order.objects.get(id=id).id
                # get nilai_transaksi from dashboard_order tables where id = id store in variable nilai_transaksi and convert to int
                nilai_transaksi = int(Order.objects.get(id=id).nilai_transaksi)
                # get komisi from produkjasa tables where id = id store in variable komisi and convert to int
                komisi = int(ProdukJasa.objects.get(id=Order.objects.get(id=id).produkjasa_id).komisi)
                # do calculation komisi * nilai_transaksi / 100 and store in variable komisi and conver to int
                komisi = int(komisi * nilai_transaksi / 100)
                # do insert to daashboard_pendapatanworker tables with workerid, orderid, nilai_komisi, tgl_transaksi
                PendapatanWorker.objects.create(workerid=Worker.objects.get(id=workernya),
                                                orderanid=Order.objects.get(id=orderannya),
                                                nilai_komisi=komisi,)
                Worker.objects.filter(id=workernya).update(pendapatankomisi=F('pendapatankomisi') + komisi)
                Order.objects.filter(id=id).update(status=new_status)
                return render(request, 'dashboard/status-orderan.html', {
                    'orderan': Order.objects.select_related('workerid', 'produkjasa', 'status').all().order_by(
                        '-tgl_order'),
                    'formubahstatus': formubahstatus(),
                    'formubahworker': formubahworker(),
            })
            else:
                Order.objects.filter(id=id).update(status=new_status)
                return render(request, 'dashboard/status-orderan.html', {
                    'orderan': Order.objects.select_related('workerid', 'produkjasa', 'status').all().order_by(
                        '-tgl_order'),
                    'formubahstatus': formubahstatus(),
                    'formubahworker': formubahworker(),
                })
            Order.objects.filter(id=id).update(status=new_status)
            return render(request, 'dashboard/status-orderan.html', {
                'orderan': Order.objects.select_related('workerid', 'produkjasa', 'status').all().order_by(
                    '-tgl_order'),
                'formubahstatus': formubahstatus(),
                'formubahworker': formubahworker(),
            })
        else:
            return HttpResponse("Form is not valid")
    return render(request, 'dashboard/status-orderan.html', {
        'orderan': Order.objects.select_related('workerid', 'produkjasa', 'status').all().order_by('-tgl_order'),
        'formubahstatus': formubahstatus(),
        'formubahworker': formubahworker(),
    })

@login_required(login_url='login')
def ubah_worker(request, id):
    if request.method == "POST":
        orderid = Order.objects.get(id=id)
        form = formubahworker(request.POST, instance=orderid)
        if form.is_valid():
            new_worker = form.cleaned_data['workerid']
            Order.objects.filter(id=id).update(workerid=new_worker)
            return render(request, 'dashboard/status-orderan.html', {
                'orderan': Order.objects.select_related('workerid', 'produkjasa', 'status').all().order_by(
                    '-tgl_order'),
                'formubahstatus': formubahstatus(),
                'formubahworker': formubahworker(),
            })
        else:
            return HttpResponse("Form is not valid")
    return render(request, 'dashboard/status-orderan.html', {
        'orderan': Order.objects.select_related('workerid', 'produkjasa', 'status').all().order_by('-tgl_order'),
        'formubahstatus': formubahstatus(),
        'formubahworker': formubahworker(),

    })

@login_required(login_url='login')
def tambahorderan(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            new_nomor_hp_customer = form.cleaned_data['nomor_hp_customer']
            new_nomor_id_ml = form.cleaned_data['nomor_id_ml']
            new_nomor_server_ml = form.cleaned_data['nomor_server_ml']
            new_rankawal = form.cleaned_data['rankawal']
            new_rankakhir = form.cleaned_data['rankakhir']
            new_nilai_transaksi = form.cleaned_data['nilai_transaksi']
            new_produkjasa = form.cleaned_data['produkjasa']
            new_status = form.cleaned_data['status']
            new_order = Order(nomor_hp_customer=new_nomor_hp_customer, nomor_id_ml=new_nomor_id_ml,
                              nomor_server_ml=new_nomor_server_ml, rankawal=new_rankawal, rankakhir=new_rankakhir,
                              nilai_transaksi=new_nilai_transaksi, produkjasa=new_produkjasa, status=new_status)
            new_order.save()
            return render(request, 'dashboard/status-orderan.html', {
                'orderan': Order.objects.select_related('workerid', 'produkjasa', 'status').all().order_by('-tgl_order'),
                'formubahstatus': formubahstatus(),
                'formubahworker': formubahworker(),
            })
        else:
            return HttpResponse("Form is not valid")
    return render(request, 'dashboard/tambah-orderan.html', {
        'form': OrderForm(),
    })

@login_required(login_url='login')
def listworker(request):
    worker = Worker.objects.all().values('id', 'nama', 'nomor_hp', 'pendapatankomisi')
    return render(request, 'dashboard/list-worker.html', {
        'worker': worker,
        'formubahworker': formubahworker(),
        'formtambahworker': formtambahworker(),
    })

@login_required(login_url='login')
def tambahworker(request):
    if request.method == "POST":
        form = formtambahworker(request.POST)
        if form.is_valid():
            new_nama = form.cleaned_data['nama']
            new_nomor_hp = form.cleaned_data['nomor_hp']
            new_worker = Worker(nama=new_nama, nomor_hp=new_nomor_hp,pendapatankomisi=0)
            new_worker.save()
            return HttpResponseRedirect(reverse('worker'))
        else:
            return HttpResponse("Form is not valid")
    return HttpResponseRedirect(reverse('worker'))


@login_required(login_url='login')
def editworker(request, id):
    if request.method == "POST":
        workerid = Worker.objects.get(id=id)
        form = formubahworker(request.POST, instance=workerid)
        if form.is_valid():
            new_nama = form.cleaned_data['nama']
            new_nomor_hp = form.cleaned_data['nomor_hp']
            Worker.objects.filter(id=id).update(nama=new_nama, nomor_hp=new_nomor_hp)
            return HttpResponseRedirect(reverse('worker'))
        else:
            return HttpResponse("Form is not valid")
    return HttpResponseRedirect(reverse('worker'))

@login_required(login_url='login')
def hapusworker(request, id):
    Worker.objects.filter(id=id).delete()
    return HttpResponseRedirect(reverse('worker'))

@login_required(login_url='login')
def penghasilanworker(request):
    # inner join worker and order where order.workerid = worker.id
    #order = Order.objects.select_related('workerid', 'produkjasa', 'status').all().filter(status=3).order_by('-tgl_order')
    # inner join worker and dashboard_pendapatanworker where dashboard_pendapatanworker.workerid = worker.id
    pendapatan = PendapatanWorker.objects.select_related('workerid', 'orderanid').all().order_by('-tgl_transaksi')
    hitungpendatapan = PendapatanWorker.objects.select_related('workerid', 'orderanid').all().aggregate(Sum('nilai_komisi'))
    countorderselesai = Order.objects.filter(status=3).count()
    return render(request, 'dashboard/penghasilan-worker.html', {
        'pendapatan': pendapatan,
        'countorderselesai': countorderselesai,
        'hitungpendatapan': hitungpendatapan,
    })

@login_required(login_url='login')
def pembayarankomisi(request):
    if request.method == "POST":
        form = formwithdrawworker(request.POST)
        if form.is_valid():
            idworker = form.data['workerid']
            new_workerid = form.cleaned_data['workerid']
            new_nilai_transaksi = form.cleaned_data['nilai_transaksi']
            new_pembayarankomisi = TransaksiWithdraw(workerid=new_workerid, nilai_transaksi=new_nilai_transaksi)
            updatekomisi = Worker.objects.filter(id=idworker).update(pendapatankomisi=0)
            new_pembayarankomisi.save()
            return render(request, 'dashboard/pembayaran-komisi.html', {
                'worker': Worker.objects.all().values('id','nama', 'pendapatankomisi'),
                'form': formwithdrawworker(),
            })
        else:
            return HttpResponse("Form is not valid")
    # select from dashboard_worker only nama and pendapatankomisi coloumn
    worker = Worker.objects.all().values('id','nama', 'pendapatankomisi')
    # totalkomisiperworker = Worker.objects.annotate(namaworker=F('nama'), pendapatankomisi=F('pendapatankomisi'))
    # totalkomisiperworker = PendapatanWorker.objects.select_related('workerid').values('workerid').annotate(idworker=F('workerid__id'),namaworker=F('workerid__nama'),total=Sum('nilai_komisi'))
    # konteks = {'totalkomisi': totalkomisiperworker, 'form': formwithdrawworker()}
    konteks = {'form': formwithdrawworker(), 'worker': worker}
    # print(totalkomisiperworker.query)
    return render(request, 'dashboard/pembayaran-komisi.html', konteks)

@login_required(login_url='login')
def aturkomisi(request):
    if request.method == "POST":
        form = formrubahkomisiprodukjasa(request.POST)
        if form.is_valid():
            idprodukjasa = form.data['idprodukjasa']
            new_komisi = form.cleaned_data['komisi']
            updatekomisi = ProdukJasa.objects.filter(id=idprodukjasa).update(komisi=new_komisi)
            return render(request, 'dashboard/atur-komisi.html', {
                'listprodukjasa': ProdukJasa.objects.all().values('id', 'nama', 'komisi'),
                'form': formrubahkomisiprodukjasa(),
                'formtambahprodukjasa': formtambahprodukjasa(),
            })
        else:
            return HttpResponse("Form is not valid")
    listprodukjasa = ProdukJasa.objects.all().values('id', 'nama', 'komisi')
    form = formrubahkomisiprodukjasa()
    return render(request, 'dashboard/atur-komisi.html', {
        'listprodukjasa': listprodukjasa,
        'form': form,
        'formtambahprodukjasa': formtambahprodukjasa(),
    })

@login_required(login_url='login')
def tambahprodukjasa(request):
    if request.method == "POST":
        form = formtambahprodukjasa(request.POST)
        if form.is_valid():
            new_nama = form.cleaned_data['nama']
            new_komisi = form.cleaned_data['komisi']
            new_produkjasa = ProdukJasa(nama=new_nama, komisi=new_komisi)
            new_produkjasa.save()
            return HttpResponseRedirect(reverse('aturkomisi'))
        else:
            return HttpResponse("Form is not valid")
    return HttpResponseRedirect(reverse('aturkomisi'))

@login_required(login_url='login')
def hapusprodukjasa(request, id):
    ProdukJasa.objects.filter(id=id).delete()
    return HttpResponseRedirect(reverse('aturkomisi'))