from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ValidationError
from .models import *

class ItemSerializer(ModelSerializer):
    class Meta:
        model=Items
        fields=[
            'name','description','category',
            'quantity','unit_price','supplier',
            'location','image','created_by','updated_by'
        ]
    def validate(self, attrs):
        fields=list(self.fields.keys())
        expected_fields = set(fields)
        provided_fields = set(attrs.keys())
        missing_fields = expected_fields - provided_fields
        if missing_fields and not missing_fields.issubset({'created_by', 'updated_by'}):
            raise ValidationError(f"Missing fields: {', '.join(missing_fields)}")
        return super().validate(attrs)
    
   
    def create(self, validated_data):
        existing_item = Items.objects.filter(
            category=validated_data['category'],
            supplier=validated_data['supplier'],
            location=validated_data['location'],
            name=validated_data['name'],
        ).first()

        if existing_item:
            existing_item.quantity += validated_data['quantity'] 
            existing_item.unit_price = validated_data['unit_price']  
            existing_item.save()  
            return existing_item  
        item = Items(**validated_data)
        item.save()
        return item

    def update(self, instance, validated_data):
        validated_data['created_by']=instance.created_by
        return super().update(instance, validated_data)