# Django
from django.db.models import (
    Sum,
    Count,
    Subquery,
    OuterRef,
    Value,
    DecimalField,
    IntegerField,
)
from django.db.models.functions import TruncDate, Coalesce
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Local apps
from apps.company.models import Company
from apps.transaction.models import Transaction
from .serializers import (
    CompanySerializer,
    SummarySerializer,
    CompanySummarySerializer,
)


class SummaryApiView(APIView):
    """
    Api View Service summary
    Description: Este servicio no recibirá ningún parámetro, pero deberá regresar un resumen de lo que se encuentra en
    la base de datos previamente importada. Por ejemplo:
        - La empresa con más ventas
        - La empresa con menos ventas
        - El precio total de las transacciones que SÍ se cobraron
        - El precio total de las transacciones que NO se cobraron
        - La empresa con más rechazos de ventas (es decir, no se cobraron)
    """

    def get_companies_by_confirmed_transactions(self, transactions_confirmed):
        companies = (
            Company.objects.filter(state=True)
            .annotate(
                amount=Coalesce(
                    Subquery(
                        transactions_confirmed.filter(company=OuterRef("pk"))
                        .values("company")
                        .annotate(amount=Sum("price"))
                        .values("amount")
                    ),
                    Value(0, output_field=DecimalField()),
                )
            )
            .order_by("-amount")
        )
        return companies

    def get_companies_by_canceled_transactions(self, canceled_transactions):
        companies = (
            Company.objects.filter(state=True)
            .annotate(
                amount=Coalesce(
                    Subquery(
                        canceled_transactions.filter(company=OuterRef("pk"))
                        .values("company")
                        .annotate(amount=Count("price"))
                        .values("amount")
                    ),
                    Value(0, output_field=IntegerField()),
                )
            )
            .order_by("-amount")
        )
        return companies

    def get(self, request, format=None):
        try:
            transactions = Transaction.objects.all()
            # Sum
            transactions_confirmed = transactions.filter(
                approval_state=True,
                transaction_state=Transaction.StateChoices.CLOSED,
            )
            companies_selling = self.get_companies_by_confirmed_transactions(
                transactions_confirmed
            )
            most_selling_company = companies_selling.first()
            least_selling_company = companies_selling.last()

            # Canceled transactions
            canceled_transactions = transactions.exclude(
                approval_state=True,
                transaction_state=Transaction.StateChoices.CLOSED,
            )
            companies_canceled = self.get_companies_by_canceled_transactions(
                canceled_transactions
            )
            most_canceled_company = companies_canceled.first()

            # Totals
            total_selling_revenue = transactions_confirmed.aggregate(
                amount=Sum("price")
            ).get("amount")

            total_canceled_revenue = canceled_transactions.aggregate(
                amount=Sum("price")
            ).get("amount")
            kwargs = {
                "most_selling_company": CompanySerializer(most_selling_company).data,
                "least_selling_company": CompanySerializer(least_selling_company).data,
                "total_selling_revenue": total_selling_revenue,
                "total_canceled_revenue": total_canceled_revenue,
                "most_canceled_company": CompanySerializer(most_canceled_company).data,
            }
            summary = SummarySerializer(data=kwargs)
            if summary.is_valid():
                return Response(summary.data, status=status.HTTP_200_OK)
            return Response(summary.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CompanyApiView(APIView):
    """
    Api View Service Company summary
    Description: Este servicio deberá recibir el ID de la empresa y nos deberá regresar la siguiente información
        - Nombre de la empresa
        - Total de transacciones que SÍ se cobraron
        - Total de transacciones que NO se cobraron
        - El día que se registraron más transacciones
    """

    def get(self, request, pk, format=None):
        try:
            company = Company.objects.get(pk=pk)
            transactions = Transaction.objects.filter(company=company)
            transactions_confirmed = transactions.filter(
                approval_state=True,
                transaction_state=Transaction.StateChoices.CLOSED,
            )
            canceled_transactions = transactions.exclude(
                approval_state=True,
                transaction_state=Transaction.StateChoices.CLOSED,
            )
            count_transactions_by_date = (
                transactions.values("transaction_date")
                .annotate(trunc_date=TruncDate("transaction_date"))
                .values("trunc_date")
                .annotate(value=Count("trunc_date"))
                .order_by("-value")
            )
            most_transaction_date = count_transactions_by_date[0].get("trunc_date")

            company_summary = {
                "company_name": company.name.title(),
                "amount_selling": transactions_confirmed.count(),
                "amount_canceled": canceled_transactions.count(),
                "most_transaction_date": most_transaction_date,
            }
            serializer = CompanySummarySerializer(data=company_summary)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Company.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
