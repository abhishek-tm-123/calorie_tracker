from django.shortcuts import render,get_object_or_404
from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework import authentication,permissions
from rest_framework.response import Response

from food_entries.models import FoodLog
from food_entries.serializers import FoodLogSerializer
from food_entries.permissions import IsOwner

from datetime import datetime
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
        

        
class FoodLogRetrieveUpdateDeleteView(APIView):
    
    authentication_classes = [authentication.BasicAuthentication]
    
    permission_classes = [IsOwner]
    
    def get(self,request,pk=None):
        
        qs = get_object_or_404(FoodLog,id=pk)
        
        self.check_object_permissions(request,qs)
        
        serializer_instance = FoodLogSerializer(qs)
        
        return Response(serializer_instance.data)
    
    def put(self,request,pk=None):
        instance = get_object_or_404(FoodLog,id=pk)
        
        self.check_object_permissions(request,instance)
        
        form_data = request.data
        
        serializer_instance = FoodLogSerializer(data=form_data,instance=instance)
        
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)
        
    def delete(self,request,pk=None):
        instance = get_object_or_404(FoodLog,id=pk)
        
        self.check_object_permissions(request,instance)
        
        instance.delete()
        
        return Response({"message":"deleted...."})

class FoodLogSummaryView(APIView):
    
    authentication_classes = [authentication.BasicAuthentication]
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request):
        
        auth_user_foodlogs = FoodLog.objects.filter(owner=request.user)
        
        response_data = {
            "todays_total":0,
            "monthly_total":0
        }
        
        cur_date = datetime.today().date()
        
        todays_total = auth_user_foodlogs.filter(created_at__date = cur_date).values("calorie").aggregate(total=Sum("calorie")).get("total")
        
        response_data["todays_total"] = todays_total
        
        return Response(response_data)