# Django
from rest_framework import serializers

# Local
from apps.company.models import Company
from apps.transaction.models import Transaction


class CompanySerializer(serializers.ModelSerializer):
    """Class serializers model company"""

    class Meta:
        model = Company
        fields = ("name", "state")


class TransactionSerializer(serializers.ModelSerializer):
    """Class serializers model transaction"""

    company = CompanySerializer()

    class Meta:
        model = Transaction
        fields = (
            "date",
            "company",
            "price",
            "transaction_state",
        )


class SummarySerializer(serializers.Serializer):
    """Serializers summary"""

    most_selling_company = CompanySerializer()
    least_selling_company = CompanySerializer()
    most_canceled_company = CompanySerializer()
    total_selling_revenue = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
    )
    total_canceled_revenue = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
    )


class CompanySummarySerializer(serializers.Serializer):
    """Serializers company summary"""

    company_name = serializers.CharField(max_length=256)
    amount_selling = serializers.IntegerField()
    amount_canceled = serializers.IntegerField()
    most_transaction_date = serializers.DateField()
