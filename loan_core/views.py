from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Loan
from .serializers import LoanCreateSerializer, LoanSerializer
from rest_framework.decorators import api_view, permission_classes

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_loan(request):
    serializer = LoanCreateSerializer(data=request.data)
    if serializer.is_valid():
        loan = serializer.save(user=request.user)  # Assign the logged-in user
        return Response(LoanSerializer(loan).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_loans(request):
    loans = Loan.objects.filter(user=request.user)
    serializer = LoanSerializer(loans, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def foreclose_loan(request, pk):
    loan = get_object_or_404(Loan, id=pk, user=request.user)  # Safer lookup

    if loan.status == 'active':
        loan.status = 'foreclosed'
        loan.save()
        return Response({'message': 'Loan foreclosed successfully'}, status=status.HTTP_200_OK)

    return Response({'error': 'Loan is already foreclosed or closed'}, status=status.HTTP_400_BAD_REQUEST)










