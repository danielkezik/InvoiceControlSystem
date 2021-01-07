# Generated by Django 3.1.4 on 2021-01-05 22:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoices_system', '0002_invoice_name_and_user_class'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='managed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clients', to='invoices_system.user'),
        ),
    ]
