from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated 
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
import logging
from rest_framework.mixins import CreateModelMixin,UpdateModelMixin,ListModelMixin
from rest_framework import viewsets
from django.core.cache import cache 

# Create your views here.

logger = logging.getLogger('Apps.Inventory')

class  ItemView(viewsets.ModelViewSet):
    queryset=Items.objects.all()
    permission_classes=[IsAuthenticated]
    serializer_class=ItemSerializer
    
    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                response={
                    "status":status.HTTP_201_CREATED,
                    "message":"Inventory Creted  Successfully"
                }
                return Response(response,status=status.HTTP_201_CREATED)
        except Exception:
            logger.error(f"Inventory Creation Failed: {serializer.errors}")
            response={
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"Inventory Creation Failed",
                "errors":serializer.errors
            }
            return Response(response)
               

    def update(self, request, *args, **kwargs):
        result = super().update(request, *args, **kwargs)
        response = {
            'status': status.HTTP_200_OK,
            "message": "Item Updated Successfully",
            "data": result.data  
        }
        return Response(response)
    
    def list(self, request, *args, **kwargs):
        try:
            cache_key = 'item_list'  
            cached_data = cache.get(cache_key)
            if cached_data is not None:
                return Response(cached_data) 
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            response = {
                'status': status.HTTP_200_OK,
                "message": "Data Fetched Successfully",
                "data": serializer.data
            }
            cache.set(cache_key, response, timeout=60 * 5)
            return Response(response)
        except Exception as e:
            return Response(str(e))

       
    
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        response = {
            'status': status.HTTP_200_OK,
            "message": "Data Deleted Successfully",
        }
        return Response(response)
    