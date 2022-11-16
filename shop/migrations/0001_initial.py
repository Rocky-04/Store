# Generated by Django 4.1.1 on 2022-10-16 12:41

import django.db.models.deletion
import mptt.fields
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('available',
                 models.BooleanField(default=True, verbose_name='Наявність')),
            ],
            options={
                'verbose_name': 'Колір',
                'verbose_name_plural': 'Кольори',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(blank=True, unique=True,
                                          verbose_name='Слаг')),
                ('picture', models.ImageField(blank=True, null=True,
                                              upload_to='photo/%Y/%m/%d/',
                                              verbose_name='Фото')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id',
                 models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent',
                 mptt.fields.TreeForeignKey(blank=True, null=True,
                                            on_delete=django.db.models.deletion.CASCADE,
                                            related_name='children',
                                            to='shop.category')),
            ],
            options={
                'verbose_name': 'Категорія',
                'verbose_name_plural': 'Категорії',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('value',
                 models.CharField(blank=True, default=None, max_length=15,
                                  null=True)),
            ],
            options={
                'verbose_name': 'Колір',
                'verbose_name_plural': 'Кольори',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True,
                                           verbose_name='Назва')),
                ('slug', models.SlugField(blank=True, unique=True,
                                          verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Країна',
                'verbose_name_plural': 'Країни',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True,
                                           verbose_name='Назва')),
                ('rate', models.IntegerField(blank=True)),
            ],
            options={
                'verbose_name': 'Валюта',
                'verbose_name_plural': 'Валюти',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                (
                    'name', models.CharField(max_length=50, verbose_name='Назва')),
                ('price',
                 models.IntegerField(default=0, verbose_name='Вартість')),
                ('order_price', models.IntegerField(blank=True, default=0,
                                                    verbose_name='Вартість замовлення')),
                ('is_active', models.BooleanField(blank=True, default=True)),
            ],
            options={
                'verbose_name': 'Вартість доставки',
                'verbose_name_plural': 'Вартість доставки',
                'ordering': ['price'],
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True,
                                           verbose_name='Назва')),
                ('slug', models.SlugField(blank=True, unique=True,
                                          verbose_name='Слаг')),
                ('picture', models.ImageField(blank=True, null=True,
                                              upload_to='photo/%Y/%m/%d/',
                                              verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Бренд',
                'verbose_name_plural': 'Бренд',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('value',
                 models.CharField(blank=True, default=None, max_length=15,
                                  null=True)),
            ],
            options={
                'verbose_name': 'Розмір',
                'verbose_name_plural': 'Розміри',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=24)),
            ],
            options={
                'verbose_name': 'Статуc',
                'verbose_name_plural': 'Статуси',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True,
                                           verbose_name='Назва')),
                ('title_two', models.CharField(blank=True, max_length=50,
                                               verbose_name='Назва 2')),
                ('slug', models.SlugField(blank=True, verbose_name='Слаг')),
                ('description', models.TextField(blank=True, default=None,
                                                 verbose_name='Опис')),
                ('is_active', models.BooleanField(blank=True, default=True)),
                ('picture', models.ImageField(blank=True, null=True,
                                              upload_to='photo/%Y/%m/%d/',
                                              verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Тегі',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200,
                                           verbose_name='Назва')),
                ('slug', models.SlugField(blank=True, unique=True,
                                          verbose_name='Слаг')),
                ('available',
                 models.BooleanField(default=True, verbose_name='Наявність')),
                ('price', models.DecimalField(decimal_places=0, default=0,
                                              max_digits=10,
                                              verbose_name='Ціна')),
                ('discount', models.DecimalField(decimal_places=0, default=0,
                                                 max_digits=10,
                                                 verbose_name='Скидка')),
                ('price_now', models.DecimalField(decimal_places=0, default=0,
                                                  max_digits=10)),
                ('description', models.TextField(blank=True, default=None,
                                                 verbose_name='Опис')),
                ('param', models.TextField(blank=True, default=None,
                                           verbose_name='Параметри')),
                ('vendorCode', models.CharField(blank=True, max_length=50,
                                                verbose_name='Артикул')),
                ('global_id', models.CharField(blank=True, max_length=50)),
                ('count_sale',
                 models.IntegerField(default=0, verbose_name='Продажів')),
                ('created_at', models.DateTimeField(auto_now_add=True,
                                                    verbose_name='Створено')),
                ('category',
                 mptt.fields.TreeForeignKey(null=True,
                                            on_delete=django.db.models.deletion.PROTECT,
                                            to='shop.category',
                                            verbose_name='Категорія')),
                ('country',
                 models.ForeignKey(blank=True, default=1, null=True,
                                   on_delete=django.db.models.deletion.SET_NULL,
                                   to='shop.country', verbose_name='Країна')),
                ('currency', models.ForeignKey(default=1, null=True,
                                               on_delete=django.db.models.deletion.SET_NULL,
                                               to='shop.currency',
                                               verbose_name='Валюта')),
                ('manufacturer',
                 models.ForeignKey(blank=True, default=1, null=True,
                                   on_delete=django.db.models.deletion.SET_NULL,
                                   related_name='manufacturer',
                                   to='shop.manufacturer',
                                   verbose_name='Виробник')),
                ('tags',
                 models.ManyToManyField(blank=True, related_name='products',
                                        to='shop.tag')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товари',
                'ordering': ['-available', '-count_sale', '-created_at',
                             'price'],
            },
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True,
                                           verbose_name='Назва')),
                ('tag', models.ForeignKey(blank=True,
                                          on_delete=django.db.models.deletion.CASCADE,
                                          to='shop.tag')),
            ],
            options={
                'verbose_name': 'Банер',
                'verbose_name_plural': 'Банери',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='AttributeSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('available',
                 models.BooleanField(default=True, verbose_name='Наявність')),
                ('product',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='attribute_size',
                                   to='shop.attributecolor')),
                ('size',
                 models.ForeignKey(blank=True, default=None, null=True,
                                   on_delete=django.db.models.deletion.CASCADE,
                                   related_name='size', to='shop.size')),
            ],
            options={
                'verbose_name': 'Розмір',
                'verbose_name_plural': 'Розміри',
            },
        ),
        migrations.CreateModel(
            name='AttributeColorImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('images', models.FileField(upload_to='images/%Y/%m/%d/',
                                            verbose_name='фото товару')),
                ('product', models.ForeignKey(default=None,
                                              on_delete=django.db.models.deletion.CASCADE,
                                              to='shop.attributecolor')),
            ],
            options={
                'verbose_name': 'Фото різновиду',
                'verbose_name_plural': 'Фото різновидів',
            },
        ),
        migrations.AddField(
            model_name='attributecolor',
            name='color',
            field=models.ForeignKey(blank=True, default=None, null=True,
                                    on_delete=django.db.models.deletion.CASCADE,
                                    related_name='color', to='shop.color'),
        ),
        migrations.AddField(
            model_name='attributecolor',
            name='product',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='attribute_color',
                to='shop.product'),
        ),
    ]
