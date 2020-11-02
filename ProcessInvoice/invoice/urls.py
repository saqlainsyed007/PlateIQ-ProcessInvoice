from django.urls import path
from invoice.views import (
    AdminListCreateInvoiceItem, AdminRetrieveUpdateInvoice,
    AdminRetrieveUpdateDestroyInvoiceItem,
    ListInvoices, RetrieveInvoice, UploadInvoice,
)

urlpatterns = [
    path('upload-invoice/', UploadInvoice.as_view(), name="upload_invoice"),
    path('invoice/', ListInvoices.as_view(), name="list_invoices"),
    path('invoice/<int:pk>', RetrieveInvoice.as_view(), name="retrieve_invoice"),
    path('admin/invoice/<int:pk>',
         AdminRetrieveUpdateInvoice.as_view(), name="retrieve_update_invoice_admin"),

    path('admin/invoice/<int:invoice_id>/invoice-item/',
         AdminListCreateInvoiceItem.as_view(), name="list_create_invoice_item_admin"),
    path('admin/invoice/<int:invoice_id>/invoice-item/<int:pk>',
         AdminRetrieveUpdateDestroyInvoiceItem.as_view(), name="retrieve_update_invoice_item_admin"),
]
