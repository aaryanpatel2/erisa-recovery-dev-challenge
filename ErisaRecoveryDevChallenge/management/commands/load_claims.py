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
                    for row in reader:
                        has_claim_fields = all(
                            key in row and row[key] for key in [
                                'id', 'patient_name', 'billed_amount', 'paid_amount', 'status', 'insurer_name', 'discharge_date'
                            ]
                        )
                        claim_obj = None
                        if has_claim_fields:
                            claims_defaults = {
                                'patient_name': row['patient_name'],
                                'billed_amount': Decimal(row['billed_amount']),
                                'paid_amount': Decimal(row['paid_amount']),
                                'status': row['status'],
                                'insurer_name': row['insurer_name'],
                                'discharge_date': datetime.strptime(row['discharge_date'], '%Y-%m-%d').date()
                            }
                            if overwrite:
                                claim_obj, _ = ClaimsModel.objects.update_or_create(
                                    id=row['id'], defaults=claims_defaults
                                )
                            else:
                                claim_obj, _ = ClaimsModel.objects.get_or_create(
                                    id=row['id'], defaults=claims_defaults
                                )
                        # If only claim details, get the claim instance by id
                        elif 'claim_id' in row and row['claim_id']:
                            try:
                                claim_obj = ClaimsModel.objects.get(id=row['claim_id'])
                            except ClaimsModel.DoesNotExist:
                                self.stderr.write(self.style.ERROR(f'Claim with id {row["claim_id"]} does not exist. Skipping details row.'))
                                continue

                        if claim_obj and 'denial_reason' in row and 'cpt_codes' in row:
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
                self.stdout.write(self.style.SUCCESS(f'Successfully loaded data from: {csv_file_path}'))
            except FileNotFoundError:
                self.stderr.write(self.style.ERROR(f'Error: CSV file not found at {csv_file_path}'))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'An error occurred: {e}'))
