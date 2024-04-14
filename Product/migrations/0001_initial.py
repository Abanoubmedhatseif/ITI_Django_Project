# Generated by Django 4.0.10 on 2024-04-13 23:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Categories', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('image', models.ImageField(upload_to='products/%y/%m/%d/')),
                ('active', models.BooleanField(default=True)),
                ('stock', models.IntegerField(default=0)),
                ('category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='Categories.category')),
            ],
        ),
    ]
