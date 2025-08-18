from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from .models import ClaimsModel

def claims_joined_view(request):
    dev = False # set True if you want to test endpoint in Bruno using JSON response
    search = request.GET.get('search', '').strip().lower()
    query = """
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
            c.id = d.claim_id
    """
    params = []
    if search:
        query += " WHERE LOWER(c.status) LIKE %s OR LOWER(c.insurer_name) LIKE %s"
        like_pattern = f"%{search}%"
        params.extend([like_pattern, like_pattern])
    query += ";"
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
        # print(results)
    if dev:
        return JsonResponse(results, safe=False)
    if request.headers.get('HX-Request') == 'true': # HTMX AJAX request sends this header and returns table otherwise regular claims page for non HTMX requests; needed otherwise page breaks and also so it shows header/footer
        return render(request, "erisa/claims_table.html", {"claims": results})
    return render(request, "erisa/claims.html", {"claims": results})
