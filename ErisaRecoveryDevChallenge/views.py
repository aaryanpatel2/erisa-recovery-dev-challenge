from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from .models import ClaimsModel
from django.http import HttpResponse

# HTMX fetch all endpoint
def claims_joined_view(request):
    dev = False # set True if you want to test endpoint in Bruno using JSON response
    search = request.GET.get('search', '').strip().lower()
    sort_by = request.GET.get('sort_by', '').strip()
    flagged_first = request.GET.get('flagged_first', '')
    # Parse sort_by for field and asc/desc
    sort_field, sort_dir = None, 'ASC'
    if ':' in sort_by:
        sort_field, sort_dir = sort_by.split(':', 1)
        sort_dir = 'DESC' if sort_dir.lower() == 'desc' else 'ASC'
    else:
        sort_field = sort_by if sort_by else None
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
            d.cpt_codes,
            c.flagged,
            c.custom_note
        FROM
            ErisaRecoveryDevChallenge_claimsmodel c
        JOIN
            ErisaRecoveryDevChallenge_claimdetailsmodel d
        ON
            c.id = d.claim_id
    """
    params = []
    where_clauses = []
    if search:
        where_clauses.append("(LOWER(c.status) LIKE %s OR LOWER(c.insurer_name) LIKE %s)")
        like_pattern = f"%{search}%"
        params.extend([like_pattern, like_pattern])
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    allowed_sorts = {
        'billed_amount': 'c.billed_amount',
        'paid_amount': 'c.paid_amount',
        'discharge_date': 'c.discharge_date'
    }
    order_clauses = []
    if flagged_first:
        order_clauses.append("c.flagged DESC")
    if sort_field in allowed_sorts:
        order_clauses.append(f"{allowed_sorts[sort_field]} {sort_dir}")
    if order_clauses:
        query += " ORDER BY " + ", ".join(order_clauses)
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


# HTMX endpoint to toggle flag for review
@require_POST
def flag_claim_view(request, claim_id):
    claim = get_object_or_404(ClaimsModel, id=claim_id)
    claim.flagged = not claim.flagged
    claim.save()
    claim_dict = re_join(claim_id)
    return render(request, "erisa/claims_table_row.html", {"claim": claim_dict})

# HTMX endpoint to update custom note
@require_POST
def note_claim_view(request, claim_id):
    claim = get_object_or_404(ClaimsModel, id=claim_id)
    note = request.POST.get("custom_note", "")
    claim.custom_note = note
    claim.save()
    # Return only the updated note span for htmx swap
    return HttpResponse(
        f'<span id="custom-note-{claim.id}" class="custom_note">{claim.custom_note or "N/A"}</span>'
    )

# helper function
def re_join(claim_id):
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
                d.cpt_codes,
                c.flagged,
                c.custom_note
            FROM
                ErisaRecoveryDevChallenge_claimsmodel c
            JOIN
                ErisaRecoveryDevChallenge_claimdetailsmodel d
            ON
                c.id = d.claim_id
            WHERE c.id = %s
        """, [claim_id])
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        return dict(zip(columns, row)) if row else {}