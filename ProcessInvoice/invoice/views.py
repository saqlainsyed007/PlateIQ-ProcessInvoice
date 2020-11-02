from django.shortcuts import render


from rest_framework import status
from rest_framework.generics import (
    ListAPIView, ListCreateAPIView, RetrieveAPIView,
    RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from invoice.models import Invoice, InvoiceItem
from invoice.serializers import (
    InvoiceSerializer, InvoiceItemSerializer,
    UploadInvoiceSerializer,
)


class UploadInvoice(APIView):

    permission_classes = []
    authentication_classes = []

    def post(self, request):
        input_serializer = UploadInvoiceSerializer(
            data=request.FILES
        )
        if not input_serializer.is_valid():
            return Response(
                input_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        invoice = Invoice.objects.create(
            scanned_invoice=input_serializer.validated_data['invoice_pdf']
        )
        invoice_serializer = InvoiceSerializer(invoice)
        return Response(invoice_serializer.data)


class ListInvoices(ListAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()


class RetrieveInvoice(RetrieveAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()


class AdminRetrieveUpdateInvoice(RetrieveUpdateAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()

    def put(self, request, pk):
        current_invoice_object = self.get_object()
        # Admin must not be allowed to change the file uploaded by the user
        request.data['scanned_invoice'] = current_invoice_object.scanned_invoice
        return super().put(request, pk)

    def patch(self, request, pk):
        current_invoice_object = self.get_object()
        # Admin must not be allowed to change the file uploaded by the user
        request.data['scanned_invoice'] = current_invoice_object.scanned_invoice
        return super().patch(request, pk)


class AdminListCreateInvoiceItem(ListCreateAPIView):

    permission_classes = []
    authentication_classes = []
    serializer_class = InvoiceItemSerializer

    def get_queryset(self):
        return InvoiceItem.objects.filter(
            invoice_id=self.kwargs['invoice_id']
        )

    def post(self, request, invoice_id):
        request.data['invoice'] = invoice_id
        return super().post(request)


class AdminRetrieveUpdateDestroyInvoiceItem(RetrieveUpdateDestroyAPIView):

    permission_classes = []
    authentication_classes = []
    serializer_class = InvoiceItemSerializer

    def get_queryset(self):
        return InvoiceItem.objects.filter(
            invoice_id=self.kwargs['invoice_id']
        )

    def put(self, request, invoice_id, pk):
        request.data['invoice'] = invoice_id
        return super().put(request)

    def patch(self, request, invoice_id, pk):
        request.data['invoice'] = invoice_id
        return super().patch(request)
