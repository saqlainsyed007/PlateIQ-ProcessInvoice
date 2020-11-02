from django.contrib import admin

from invoice.models import Invoice, InvoiceItem


class InvoiceItemInline(admin.StackedInline):
    model = InvoiceItem
    extra = 1


class InvoiceAdmin(admin.ModelAdmin):
    model = Invoice
    inlines = [
        InvoiceItemInline,
    ]
    list_display = (
        "id", "invoice_number", "is_digitized", "purchase_date",
        "buyer_name", "biller_name", "total", "discount", "amount",
    )
    search_fields = (
        'invoice_number', 'buyer_name', 'biller_name',
    )
    list_filter = (
        'buyer_name', 'biller_name', "purchase_date",
        "created", "updated",
    )
    readonly_fields = ("created", "updated", )


admin.site.register(Invoice, InvoiceAdmin)
