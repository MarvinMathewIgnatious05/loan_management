from rest_framework import serializers
from .models import Loan

class LoanSerializer(serializers.ModelSerializer):
    emi = serializers.SerializerMethodField()
    total_interest = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = ['id', 'amount', 'interest_rate', 'tenure_months', 'start_date', 'status', 'emi', 'total_interest']

    def get_emi(self, obj):
        return obj.calculate_monthly_installment()

    def get_total_interest(self, obj):
        return obj.total_interest_payable()


class LoanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['amount', 'interest_rate', 'tenure_months']



















# from rest_framework import serializers
# from .models import Loan
#
# class LoanSerializer(serializers.ModelSerializer):
#     emi = serializers.SerializerMethodField()
#     total_interest = serializers.SerializerMethodField()
#     total_amount = serializers.SerializerMethodField()
#     payment_schedule = serializers.SerializerMethodField()
#     amount_remaining = serializers.SerializerMethodField()
#     next_due_date = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Loan
#         fields = ['loan_id', 'amount', 'interest_rate', 'tenure_months', 'start_date', 'status',
#                   'emi', 'total_interest', 'total_amount', 'payment_schedule', 'amount_paid', 'amount_remaining', 'next_due_date']
#
#     def get_emi(self, obj):
#         return obj.calculate_monthly_installment()
#
#     def get_total_interest(self, obj):
#         return obj.total_interest_payable()
#
#     def get_total_amount(self, obj):
#         return obj.total_amount_payable()
#
#     def get_payment_schedule(self, obj):
#         return obj.generate_payment_schedule()
#
#     def get_amount_remaining(self, obj):
#         return round(obj.total_amount_payable() - obj.amount_paid, 2)
#
#     def get_next_due_date(self, obj):
#         """Get next due date if loan is active"""
#         if obj.status == 'ACTIVE':
#             return obj.generate_payment_schedule()[0]['due_date']  # Next installment date
#         return None
#
# class LoanCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Loan
#         fields = ['amount', 'interest_rate', 'tenure_months']
