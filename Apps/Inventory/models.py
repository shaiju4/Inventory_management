from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    category_name=models.CharField(max_length=200)
    status=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.category_name


class Supplier(models.Model):
    supplier_name=models.CharField(max_length=100)
    status=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.supplier_name
    
class Location(models.Model):
    location_name=models.CharField(max_length=100)
    status=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.location_name
    
    
    
class Items(models.Model):
    name=models.CharField(max_length=200)
    description=models.CharField(max_length=1000)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    unit_price=models.FloatField()
    total_value=models.FloatField(editable=False)
    supplier=models.ForeignKey(Supplier,on_delete=models.SET_NULL,null=True)
    location=models.ForeignKey(Location,on_delete=models.CASCADE)
    status=models.BooleanField(default=True)
    image=models.ImageField(max_length=200,upload_to="Items/")
    created_by=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="user_create")
    updated_by=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="user_update")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    
    def save(self,*args, **kwargs):
        if not self.category.status:
            raise ValidationError(f"Cannot save item: Category '{self.category.category_name}' is not active.")
        if not self.supplier.status:
            raise ValidationError(f"Cannot save item: Supplier '{self.supplier.supplier_name}' is not active.")
        self.total_value=self.quantity*self.unit_price
        return super().save(*args, **kwargs)