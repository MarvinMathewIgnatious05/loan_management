from django.db import models
from django.conf import settings
from decimal import Decimal

# Create your models here.



class Loan(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('foreclosed', 'Foreclosed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.FloatField()
    tenure_months = models.IntegerField()
    start_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def calculate_monthly_installment(self):
        """Calculate EMI using the standard EMI formula."""
        P = self.amount
        r = Decimal(self.interest_rate / 100 / 12)  # Monthly interest rate
        n = self.tenure_months

        if r > 0:
            emi = (P * r * (1 + r) ** n) / ((1 + r) ** n - 1)
        else:
            emi = P / n  # If interest rate is zero

        return round(emi, 2)

    def total_interest_payable(self):
        """Calculate total interest over the loan period."""
        return round(self.calculate_monthly_installment() * self.tenure_months - self.amount, 2)

    def foreclose_loan(self):
        """Foreclose loan and calculate remaining balance with penalty."""
        if self.status == 'active':
            penalty = 0.02 * self.amount  # 2% foreclosure penalty
            self.status = 'foreclosed'
            self.save()
            return round(self.amount + self.total_interest_payable() - penalty, 2)
        return 0
























