from django.urls import path
from .views import create_loan, list_loans, foreclose_loan

urlpatterns = [
    path('loans/', list_loans, name='loans'),
    path('loans/add/', create_loan, name='loan-create'),
    path('loans/foreclose/<int:pk>/', foreclose_loan, name='loan-foreclose'),
]