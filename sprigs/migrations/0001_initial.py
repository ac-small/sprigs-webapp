# Generated by Django 2.1.2 on 2020-03-25 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=500)),
                ('merchant', models.CharField(max_length=400)),
                ('flyer_id', models.CharField(max_length=200)),
                ('price_units', models.CharField(max_length=200)),
                ('sale_price', models.CharField(max_length=50)),
                ('start_date', models.DateTimeField(verbose_name='start date')),
                ('end_date', models.DateTimeField(verbose_name='end date')),
            ],
        ),
        migrations.CreateModel(
            name='Product_Classification',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('classification', models.CharField(max_length=200)),
            ],
        ),
    ]
