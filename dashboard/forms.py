from django import forms
from .models import Order, Worker, ProdukJasa, statusorderan, TransaksiWithdraw

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['produkjasa','nomor_hp_customer', 'nomor_id_ml', 'nomor_server_ml', 'rankawal', 'rankakhir', 'nilai_transaksi', 'status']
        labels = {
            'produkjasa': 'Produk/Jasa',
            'nomor_hp_customer': 'Nomor HP Customer',
            'nomor_id_ml': 'Nomor ID ML',
            'nomor_server_ml': 'Nomor Server ML',
            'rankawal': 'Rank Awal',
            'rankakhir': 'Rank Akhir',
            'nilai_transaksi': 'Nilai Transaksi',
            'status': 'Status',
        }
        widgets = {
            'produkjasa': forms.Select(attrs={'class': 'form-control'}),
            'nomor_hp_customer': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '6286576465', 'type': 'number'}),
            'nomor_id_ml': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: 123456789',  'type': 'number'}),
            'nomor_server_ml': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: 2353','type': 'number'}),
            'rankawal': forms.Select(attrs={'class': 'form-control'}),
            'rankakhir': forms.Select(attrs={'class': 'form-control'}),
            'nilai_transaksi': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
            'status': forms.HiddenInput(attrs={'class': 'form-control', 'value': '1'}),

        }

class formubahstatus(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        labels = {
            'status': 'Status',
        }
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class formubahworkerorderan(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['workerid']
        labels = {
            'workerid': 'Worker',
        }
        widgets = {
            'workerid': forms.Select(attrs={'class': 'form-control'}),
        }

class formwithdrawworker(forms.ModelForm):
    class Meta:
        model = TransaksiWithdraw
        fields = ['workerid', 'nilai_transaksi']
        labels = {
            'workerid': 'worker', 'nilai_transaksi': 'nilaitransaksi',
        }
        widgets = {
            'workerid': forms.HiddenInput(attrs={'class': 'form-control', 'type': 'number'}),
            'nilai_transaksi': forms.HiddenInput(attrs={'class': 'form-control', 'type': 'number'}),
        }

class formrubahkomisiprodukjasa(forms.ModelForm):
    class Meta:
        model = ProdukJasa
        fields = ['komisi']
        labels = {
            'komisi': 'Komisi'
        }
        widgets = {
            'komisi': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'})
        }

class formtambahprodukjasa(forms.ModelForm):
    class Meta:
        model = ProdukJasa
        fields = ['nama', 'komisi']
        labels = {
            'nama': 'Produk/Jasa', 'komisi': 'Komisi'
        }
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'komisi': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'})
        }

class formubahworker(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['nama', 'nomor_hp']
        labels = {
            'nama': 'Nama', 'nomor_hp': 'Nomor HP'
        }
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'nomor_hp': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'})
        }

class formtambahworker(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['nama', 'nomor_hp']
        labels = {
            'nama': 'Nama', 'nomor_hp': 'Nomor HP'
        }
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'nomor_hp': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'})
        }