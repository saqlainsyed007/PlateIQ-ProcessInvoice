# Generated by Django 2.2.12 on 2020-11-02 17:37

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scanned_invoice', models.FileField(help_text='Invoice image upload.', upload_to='scanned_invoices/')),
                ('invoice_number', models.CharField(blank=True, help_text='A unique number per biller to identify the invoice.', max_length=32)),
                ('purchase_date', models.DateTimeField(blank=True, help_text='Date on which the goods were purchased.', null=True)),
                ('buyer_name', models.CharField(blank=True, help_text='Name of the buyer.', max_length=256)),
                ('biller_name', models.CharField(blank=True, help_text='Name of the biller.', max_length=256)),
                ('is_digitized', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'invoice',
            },
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.CharField(help_text='An identifier of the item purchased. Could be a barcode, article number etc.', max_length=64)),
                ('item_name', models.CharField(help_text='Name of the item purchased.', max_length=256)),
                ('purchase_quantity', models.IntegerField(help_text='Number of items purchased.', validators=[django.core.validators.MinValueValidator(1)])),
                ('price', models.DecimalField(decimal_places=4, help_text='Unit price of the item before discount.', max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01000000000000000020816681711721685132943093776702880859375'))])),
                ('discounted_price', models.DecimalField(decimal_places=4, help_text='Unit price of the item after discount.', max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01000000000000000020816681711721685132943093776702880859375'))])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('invoice', models.ForeignKey(help_text='Reference of the invoice to which this item belongs.', on_delete=django.db.models.deletion.CASCADE, to='invoice.Invoice')),
            ],
            options={
                'db_table': 'invoice_item',
            },
        ),
        migrations.AddConstraint(
            model_name='invoiceitem',
            constraint=models.CheckConstraint(check=models.Q(purchase_quantity__gte=1), name='valid_purchase_quantity_constraint'),
        ),
        migrations.AddConstraint(
            model_name='invoiceitem',
            constraint=models.CheckConstraint(check=models.Q(price__gte=0.01), name='valid_price_constraint'),
        ),
        migrations.AddConstraint(
            model_name='invoiceitem',
            constraint=models.CheckConstraint(check=models.Q(discounted_price__gte=0.01), name='valid_discounted_price_constraint'),
        ),
    ]