# Generated by Django 5.2 on 2025-06-03 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qlbh', '0002_remove_khachhang_ch_remove_sanpham_ch_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hoadon',
            name='san_phams',
            field=models.ManyToManyField(through='qlbh.CTHD', to='qlbh.sanpham'),
        ),
    ]
