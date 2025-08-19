from django.db import models

class ClaimsModel(models.Model):
    id = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=100)
    billed_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('paid', 'Paid'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ], db_index=True)
    insurer_name = models.CharField(max_length=100, db_index=True)
    discharge_date = models.DateField()
    flagged = models.BooleanField(default=False)
    custom_note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.patient_name


class ClaimDetailsModel(models.Model):
    claim = models.OneToOneField(
    ClaimsModel,
        to_field='id',
        db_column='claim_id',
        on_delete=models.CASCADE,
        primary_key=True
    )
    denial_reason = models.CharField(max_length=255)
    cpt_codes = models.CharField(max_length=25)

    def __str__(self):
        return str(self.claim_id)
