# Python
import csv
import os

# Django
from django.core.management.base import BaseCommand

# Local apps
from apps.company.models import Company
from apps.transaction.models import Transaction


class Command(BaseCommand):
    help = "Import transactions"

    def handle(self, *args, **options):
        import_transaction()
        self.stdout.write(self.style.SUCCESS("Successfully init import!"))


def import_transaction():
    path = os.path.dirname(__file__) + "/../data/data-transaction.csv"
    with open(path, encoding="utf8") as read_file:
        csv_reader = csv.reader(read_file, delimiter=",")
        next(csv_reader)
        for row in csv_reader:
            try:
                company_name, price, date, transaction_state, approval_state = row
                # Clean values
                price = float(price) / 100
                approval_state = approval_state.lower() == "true"
                # Insert
                company, created = Company.objects.get_or_create(
                    name=company_name.upper()
                )
                Transaction.objects.create(
                    price=price,
                    transaction_date=date,
                    transaction_state=transaction_state,
                    approval_state=approval_state,
                    company=company,
                )
            except Exception as error:
                print(f"{error} | {row}")
