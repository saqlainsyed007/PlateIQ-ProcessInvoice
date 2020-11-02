from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Sum
from dynamic_validator import ModelFieldRequiredMixin


class Invoice(models.Model):
    """
        This model is used to store the invoice information.
    """
    scanned_invoice = models.FileField(
        null=False,
        upload_to="scanned_invoices/",
        help_text="Invoice image upload.",
    )

    # This can be made unique per biller based on the ability to
    # identify a unique biller.
    invoice_number = models.CharField(
        max_length=32, blank=True,
        help_text="A unique number per biller to identify the invoice.",
    )

    purchase_date = models.DateTimeField(
        blank=True, null=True,
        help_text="Date on which the goods were purchased.",
    )

    # Buyer can be a separate model with more details if required.
    buyer_name = models.CharField(
        max_length=256, blank=True,
        help_text="Name of the buyer.",
    )

    # Biller can be a separate model with more details if required.
    biller_name = models.CharField(
        max_length=256, blank=True,
        help_text="Name of the biller.",
    )

    is_digitized = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'invoice'

    def __str__(self):
        return f"{self.invoice_number} - {self.buyer_name}"

    @property
    def total(self):
        if (
            hasattr(self, 'invoiceitem_set') and
            self.invoiceitem_set.all()
        ):
            return Invoice.objects.filter(
                pk=self.pk
            ).annotate(
                order_total=Sum(
                    F("invoiceitem__price") *
                    F("invoiceitem__purchase_quantity"),
                    output_field=models.DecimalField(),
                )
            )[0].order_total
        return Decimal("0.0")


    @property
    def discount(self):
        if (
            hasattr(self, 'invoiceitem_set') and
            self.invoiceitem_set.all()
        ):
            return Invoice.objects.filter(
                pk=self.pk
            ).annotate(
                total_discount=Sum(
                    (F("invoiceitem__price") - F("invoiceitem__discounted_price")) *
                    F("invoiceitem__purchase_quantity"),
                    output_field=models.DecimalField(),
                )
            )[0].total_discount
        return Decimal("0.0")

    @property
    def amount(self):
        if (
            hasattr(self, 'invoiceitem_set') and
            self.invoiceitem_set.all()
        ):
            return Invoice.objects.filter(
                pk=self.pk
            ).annotate(
                total_amount=Sum(
                    F("invoiceitem__discounted_price") *
                    F("invoiceitem__purchase_quantity"),
                    output_field=models.DecimalField(),
                )
            )[0].total_amount
        return Decimal("0.0")


class InvoiceItem(models.Model):
    """
        This model is used to store the details
        of each item in the Invoice.
    """
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        help_text="Reference of the invoice to which this item belongs."
    )
    item_id = models.CharField(
        max_length=64,
        help_text=(
            "An identifier of the item purchased. "
            "Could be a barcode, article number etc."
        ),
    )
    item_name = models.CharField(
        max_length=256,
        help_text="Name of the item purchased.",
    )
    purchase_quantity = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Number of items purchased.",
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=4,
        validators=[MinValueValidator(Decimal(0.01))],
        help_text="Unit price of the item before discount.",
    )
    discounted_price = models.DecimalField(
        max_digits=10, decimal_places=4,
        validators=[MinValueValidator(Decimal(0.01))],
        help_text="Unit price of the item after discount.",
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'invoice_item'
        constraints = [
            models.CheckConstraint(
                check=models.Q(purchase_quantity__gte=1),
                name="valid_purchase_quantity_constraint",
            ),
            models.CheckConstraint(
                check=models.Q(price__gte=0.01),
                name="valid_price_constraint",
            ),
            models.CheckConstraint(
                check=models.Q(discounted_price__gte=0.01),
                name="valid_discounted_price_constraint",
            ),
        ]

    @property
    def discount(self):
        return self.price - self.discounted_price
