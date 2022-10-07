# Generated by Django 4.1.1 on 2022-10-03 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProdukJasa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(blank=True, max_length=15, null=True)),
                ('komisi', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='rankML',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank1', models.CharField(blank=True, max_length=50, null=True)),
                ('rank2', models.CharField(blank=True, max_length=50, null=True)),
                ('rank3', models.CharField(blank=True, max_length=50, null=True)),
                ('harga', models.IntegerField()),
                ('urutan', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='statusorderan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keterangan', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=15)),
                ('nomor_hp', models.CharField(max_length=15)),
                ('pendapatankomisi', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TransaksiWithdraw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tgl_transaksi', models.DateTimeField(auto_now_add=True)),
                ('nilai_transaksi', models.IntegerField()),
                ('workerid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.worker')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tgl_order', models.DateTimeField(auto_now_add=True)),
                ('nomor_hp_customer', models.CharField(max_length=15)),
                ('nomor_id_ml', models.CharField(max_length=15)),
                ('nomor_server_ml', models.CharField(max_length=15)),
                ('nilai_transaksi', models.IntegerField()),
                ('produkjasa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboard.produkjasa')),
                ('rankakhir', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='rankakhir', to='dashboard.rankml')),
                ('rankawal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='rankawal', to='dashboard.rankml')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboard.statusorderan')),
                ('workerid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboard.worker')),
            ],
        ),
    ]
