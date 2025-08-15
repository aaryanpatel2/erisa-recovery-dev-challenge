import csv
from datetime import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from ErisaRecoveryDevChallenge.models import ClaimsModel, ClaimDetailsModel

class Command(BaseCommand):
    help = 'Loads claims data from a CSV file into ClaimsModel.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')
        parser.add_argument('--overwrite', action='store_true', help='Overwrite existing records')

    def handle(self, **options):
        csv_file_path = options['csv_file']
        overwrite = options['overwrite']
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter='|')
                first_row = next(reader)
                file.seek(0)
                reader = csv.DictReader(file, delimiter='|')

                is_claims = set(['id', 'patient_name', 'billed_amount', 'paid_amount', 'status', 'insurer_name', 'discharge_date']).issubset(first_row.keys())
                is_details = set(['id', 'claim_id', 'denial_reason', 'cpt_codes']).issubset(first_row.keys())

                if is_claims and not is_details:
                    for row in reader:
                        claims_defaults = {
                            'patient_name': row['patient_name'],
                            'billed_amount': Decimal(row['billed_amount']),
                            'paid_amount': Decimal(row['paid_amount']),
                            'status': row['status'],
                            'insurer_name': row['insurer_name'],
                            'discharge_date': datetime.strptime(row['discharge_date'], '%Y-%m-%d').date()
                        }
                        if overwrite:
                            ClaimsModel.objects.update_or_create(
                                id=row['id'], defaults=claims_defaults
                            )
                        else:
                            ClaimsModel.objects.get_or_create(
                                id=row['id'], defaults=claims_defaults
                            )
                    self.stdout.write(self.style.SUCCESS(f'Success: Loaded claims data from: {csv_file_path}'))
                elif is_details:
                    for row in reader:
                        try:
                            claim_obj = ClaimsModel.objects.get(id=row['claim_id'])
                        except ClaimsModel.DoesNotExist:
                            self.stderr.write(self.style.ERROR(f'Error: Load claims list first before loading claim details'))
                            break
                        details_defaults = {
                            'denial_reason': row['denial_reason'],
                            'cpt_codes': row['cpt_codes']
                        }
                        if overwrite:
                            ClaimDetailsModel.objects.update_or_create(
                                claim=claim_obj, defaults=details_defaults
                            )
                        else:
                            ClaimDetailsModel.objects.get_or_create(
                                claim=claim_obj, defaults=details_defaults
                            )
                    self.stdout.write(self.style.SUCCESS(f'Success: Loaded claim details data from: {csv_file_path}'))
                else:
                    self.stderr.write(self.style.ERROR('Error: CSV file format not recognized.'))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'Error: CSV file not found at {csv_file_path}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {e}'))
