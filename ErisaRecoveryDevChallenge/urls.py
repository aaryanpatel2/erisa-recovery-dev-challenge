from django.urls import path
from .views import claims_joined_view, flag_claim_view, note_claim_view

urlpatterns = [
    path('', claims_joined_view, name='claims'),
    path('api/claims/', claims_joined_view, name='claims-joined'),
    path('api/claims/flag/<int:claim_id>/', flag_claim_view, name='flag-claim'),
    path('api/claims/note/<int:claim_id>/', note_claim_view, name='note-claim'),
]
