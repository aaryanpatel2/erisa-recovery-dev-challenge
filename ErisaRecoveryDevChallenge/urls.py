from django.urls import path
from .views import claims_joined_view

urlpatterns = [
    path('', claims_joined_view, name='claims'),
    path('api/claims/', claims_joined_view, name='claims-joined'),
]
