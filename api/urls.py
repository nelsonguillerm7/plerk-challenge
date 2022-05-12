# Django
from django.urls import path

# Local apps
from .views import SummaryApiView, CompanyApiView

urlpatterns = [
    path("summary/", SummaryApiView.as_view(), name="summary"),
    path("company/<int:pk>/", CompanyApiView.as_view(), name="company"),
]
