# Generated by Django 4.2.5 on 2023-09-17 05:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ordered',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('shipping', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('date', models.DateField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(blank=True, max_length=200, null=True)),
                ('district', models.CharField(blank=True, max_length=200, null=True)),
                ('town', models.CharField(blank=True, max_length=200, null=True)),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'db_table': 'ordered',
            },
        ),
        migrations.CreateModel(
            name='StatusOrder',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('content', models.CharField(default='Waiting For Confirmation', max_length=200)),
            ],
            options={
                'db_table': 'StatusOrder',
            },
        ),
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('discount_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('expiration_date', models.DateField()),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=200, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('province', models.CharField(blank=True, max_length=100, null=True)),
                ('district', models.CharField(blank=True, max_length=100, null=True)),
                ('town', models.CharField(blank=True, max_length=100, null=True)),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
                ('customer', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('unit', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('category', models.CharField(max_length=150)),
                ('quantity', models.IntegerField()),
                ('img', models.ImageField(null=True, upload_to='product-img')),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('shipping', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('voucher', models.ManyToManyField(blank=True, to='core.voucher')),
            ],
            options={
                'db_table': 'product',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('code', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('shipping', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ordered')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.product')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.statusorder')),
            ],
            options={
                'db_table': 'order_item',
            },
        ),
        migrations.AddField(
            model_name='ordered',
            name='customer',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='core.user'),
        ),
        migrations.CreateModel(
            name='new',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_date', models.DateTimeField(auto_now_add=True)),
                ('post_content', models.TextField()),
                ('img', models.ImageField(null=True, upload_to='news-img')),
                ('title', models.TextField()),
                ('post_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.user')),
            ],
            options={
                'db_table': 'news',
            },
        ),
        migrations.CreateModel(
            name='Liked',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.user')),
                ('product', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.product')),
            ],
            options={
                'db_table': 'liked',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('body', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('commentor', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='core.product')),
            ],
            options={
                'db_table': 'comment',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.user')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.product')),
            ],
            options={
                'db_table': 'cart',
            },
        ),
    ]
