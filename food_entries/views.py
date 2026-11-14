from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import authentication,permissions
from rest_framework.response import Response

from food_entries.models import FoodLog
from food_entries.serializers import FoodLogSerializer
# Create your views here.

class FoodLogListCreateView(APIView):
    
    authentication_classes = [authentication.BasicAuthentication]
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request):
        
        auth_user = request.user
        
        qs = FoodLog.objects.filter(owner=auth_user)
        
        serializer_instance = FoodLogSerializer(qs,many=True)
        
        return Response(serializer_instance.data)
    
    def post(self,request):
        
        auth_user = request.user
        
        form_data = request.data
        
        serializer_instance = FoodLogSerializer(data=form_data)
        
        if serializer_instance.is_valid():
            
            serializer_instance.save(owner=auth_user)
            
            return Response(serializer_instance.data)
        
        else:
            return Response(serializer_instance.errors)
        
        
        