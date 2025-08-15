from django.db import connection
from django.http import JsonResponse

def claims_joined_view(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                c.id AS id,
                c.patient_name,
                c.billed_amount,
                c.paid_amount,
                c.status,
                c.insurer_name,
                c.discharge_date,
                d.denial_reason,
                d.cpt_codes
            FROM
                ErisaRecoveryDevChallenge_claimsmodel c
            JOIN
                ErisaRecoveryDevChallenge_claimdetailsmodel d
            ON
                c.id = d.claim_id;
        """)
        columns = [col[0] for col in cursor.description]
        results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
    return JsonResponse(results, safe=False)
