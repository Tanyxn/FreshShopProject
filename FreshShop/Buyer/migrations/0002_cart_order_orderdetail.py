# Generated by Django 2.2.1 on 2019-07-30 02:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=32, verbose_name='订单编号')),
                ('goods_count', models.IntegerField(verbose_name='订单商品数量')),
                ('order_price', models.FloatField(verbose_name='订单总价')),
                ('order_status', models.IntegerField(default=1, verbose_name='订单状态')),
                ('order_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Buyer.Address', verbose_name='订单地址')),
                ('order_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.Buyer', verbose_name='订单用户')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_id', models.IntegerField(verbose_name='商品id')),
                ('goods_store', models.CharField(max_length=32, verbose_name='商品店铺')),
                ('goods_name', models.CharField(max_length=32, verbose_name='商品名称')),
                ('goods_price', models.FloatField(verbose_name='商品单价')),
                ('goods_number', models.IntegerField(verbose_name='商品购买数量')),
                ('goods_total', models.FloatField(verbose_name='商品总价')),
                ('goods_image', models.ImageField(upload_to='', verbose_name='商品详情')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.Order', verbose_name='订单id')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=32, verbose_name='店铺名称')),
                ('goods_id', models.IntegerField(verbose_name='商品id')),
                ('goods_name', models.CharField(max_length=32, verbose_name='商品名称')),
                ('goods_price', models.FloatField(verbose_name='商品价格')),
                ('goods_num', models.IntegerField(verbose_name='商品数量')),
                ('goods_image', models.ImageField(upload_to='', verbose_name='商品图片')),
                ('total', models.FloatField(verbose_name='总价')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.Buyer', verbose_name='用户id')),
            ],
        ),
    ]
