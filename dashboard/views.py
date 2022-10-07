from django.db.models import Sum
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Order, Worker, ProdukJasa, statusorderan, PendapatanWorker
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
import json
import requests
from .forms import OrderForm, formubahstatus, formubahworker

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


def statusorderan(request):
    # inner join worker and order where order.workerid = worker.id
    order = Order.objects.select_related('workerid', 'produkjasa', 'status').all().order_by('-tgl_order')
    nomorid = Order.objects.values_list('nomor_id_ml', flat=True).distinct().order_by('-tgl_order')
    return render(request, 'dashboard/status-orderan.html', {
        'orderan': order,
        'formubahstatus': formubahstatus(),
        'formubahworker': formubahworker(),
    })


def ubah_status(request, id):
    if request.method == "POST":
        orderid = Order.objects.get(id=id)
        form = formubahstatus(request.POST, instance=orderid)
        if form.is_valid():
            new_status = form.cleaned_data['status']
            print(str(new_status))
            nilai_transaksi = Order.objects.get(id=id).nilai_transaksi
            if str(new_status) == 'Selesai':
                print('kena disini 1')
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
                Order.objects.filter(id=id).update(status=new_status)
                return render(request, 'dashboard/status-orderan.html', {
                    'orderan': Order.objects.select_related('workerid', 'produkjasa', 'status').all().order_by(
                        '-tgl_order'),
                    'formubahstatus': formubahstatus(),
                    'formubahworker': formubahworker(),
            })
            else:
                print('kena disini 2')
                Order.objects.filter(id=id).update(status=new_status)
                return render(request, 'dashboard/status-orderan.html', {
                    'orderan': Order.objects.select_related('workerid', 'produkjasa', 'status').all().order_by(
                        '-tgl_order'),
                    'formubahstatus': formubahstatus(),
                    'formubahworker': formubahworker(),
                })
            print('kena disini 3')
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

def penghasilanworker(request):
    # inner join worker and order where order.workerid = worker.id
    #order = Order.objects.select_related('workerid', 'produkjasa', 'status').all().filter(status=3).order_by('-tgl_order')
    # inner join worker and dashboard_pendapatanworker where dashboard_pendapatanworker.workerid = worker.id
    pendapatan = PendapatanWorker.objects.select_related('workerid', 'orderanid').all().order_by('-tgl_transaksi')
    return render(request, 'dashboard/penghasilan-worker.html', {
        'pendapatan': pendapatan,
    })