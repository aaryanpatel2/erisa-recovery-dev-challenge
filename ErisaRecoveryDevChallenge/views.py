from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from .models import ClaimsModel

def claims_joined_view(request):
    dev = False # set True if you want to test endpoint in Bruno using JSON response
    search = request.GET.get('search', '').strip().lower()
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

    # Python-side filtering for HTMX search
    if search:
        def match(claim):
            return any(
                search in str(claim.get(field, '')).lower()
                for field in [
                    'status', 'insurer_name'
                ]
            )
        results = list(filter(match, results))
    if dev:
        return JsonResponse(results, safe=False)
    if request.headers.get('HX-Request') == 'true': # HTMX AJAX request sends this header and returns table otherwise regular claims page for non HTMX requests; needed otherwise page breaks and also so it shows header/footer
        return render(request, "erisa/claims_table.html", {"claims": results})
    return render(request, "erisa/claims.html", {"claims": results})
