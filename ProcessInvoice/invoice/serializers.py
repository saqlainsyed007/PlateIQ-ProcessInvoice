from rest_framework import serializers

from invoice.models import Invoice, InvoiceItem


class UploadInvoiceSerializer(serializers.Serializer):
    invoice_pdf = serializers.FileField(required=True)


class InvoiceItemSerializer(serializers.ModelSerializer):
    discount = serializers.ReadOnlyField()
    created = serializers.ReadOnlyField()
    updated = serializers.ReadOnlyField()

    class Meta:
        model = InvoiceItem
        fields = "__all__"

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        price = validated_data.get('price')
        discounted_price = validated_data.get('discounted_price')
        if not price or not discounted_price:
            instance = self.instance or InvoiceItem.objects.get(id=attrs['id'])
            price = validated_data.get('price', instance.price)
            discounted_price = validated_data.get(
                'discounted_price', instance.discounted_price
            )
        if price < discounted_price:
            raise serializers.ValidationError({
                'price': "Price cannot be less than discounted price",
                'discounted_price': "discounted price cannot be greater than price"
            })
        return validated_data


class InvoiceSerializer(serializers.ModelSerializer):

    invoiceitem_set = InvoiceItemSerializer(
        many=True, read_only=True
    )
    invoice_number = serializers.CharField(required=True)
    buyer_name = serializers.CharField(required=True)
    biller_name = serializers.CharField(required=True)
    discount = serializers.ReadOnlyField()
    amount = serializers.ReadOnlyField()
    total = serializers.ReadOnlyField()
    created = serializers.ReadOnlyField()
    updated = serializers.ReadOnlyField()

    class Meta:
        model = Invoice
        fields = [
            "id", "scanned_invoice", "invoice_number", "purchase_date",
            "buyer_name", "biller_name", "is_digitized", "created",
            "updated", "discount", "amount", "total", "invoiceitem_set",
        ]

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if attrs.get('is_digitized'):
            missing_fields_error_map = {}
            for field in [
                "invoice_number", "purchase_date", "buyer_name", "biller_name"
            ]:
                if not attrs.get(
                    field, getattr(self.instance, field, None)
                ):
                    missing_fields_error_map[field] = "This field is required for digitization"
            if missing_fields_error_map:
                raise serializers.ValidationError(missing_fields_error_map)
            if not self.instance or not self.instance.invoiceitem_set.all():
                raise serializers.ValidationError(
                    "Cannot mark digitized without any Invoice Items"
                )
        return validated_data

    def update(self, instance, validated_data):
        # Scanned Invoice should never be updated.
        validated_data.pop('scanned_invoice', None)
        return super().update(instance, validated_data)
