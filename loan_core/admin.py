from django.contrib import admin
from .models import Loan

class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'interest_rate', 'tenure_months', 'status', 'start_date')
    list_filter = ('status', 'start_date')
    # search_fields = ('user__username', 'user__email')

admin.site.register(Loan, LoanAdmin)
