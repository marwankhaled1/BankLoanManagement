from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.query import QuerySet

# Create your models here.

# models.py

from django.contrib.auth.models import AbstractUser,User
from django.db import models

class User(AbstractUser):
    class UserType(models.TextChoices):
        Bank_Employee = 'BANK_EMPLOYEE', 'Bank_Employee'
        Loan_Provider = 'LOAN_PROVIDER', 'Loan_Provider'
        Customer = 'CUSTOMER', 'Customer'


    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    type = models.CharField(max_length=50, choices=UserType.choices, default=UserType.Bank_Employee)

   
class ProviderMore(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    total_budget = models.DecimalField(max_digits=10, decimal_places=2)



class LoanProviderManager(models.Manager):
    def get_queryset(self,*args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.UserType.Loan_Provider)   




class LoanProvider(User):
    objects=LoanProviderManager()
    class Meta:
        proxy=True
    
    @property
    def more(self):
        return self.providermore

    def save(self,*args, **kwargs):
        if not self.pk:
            self.type=User.UserType.Loan_Provider

        return super().save(*args, **kwargs)

    

class CustomerManager(models.Manager):
    def get_queryset(self,*args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.UserType.Customer)


class CustomerMore(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    

class Customer(User):
    objects=CustomerManager()
    
    class Meta:
        proxy=True
    
    @property
    def more(self):
        return self.customermore

    def save(self,*args, **kwargs):
        if not self.pk:
            self.type=User.UserType.Customer

        return super().save(*args, **kwargs)

 

    



# class Loan(models.Model):
#     class LoanState(models.TextChoices):
#         PENDING = 'PENDING', 'Pending'
#         REQUESTED = 'REQUESTED', 'Requested'
#         REJECTED = 'REJECTED', 'Rejected'

#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
#     loan_provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     loan_term = models.IntegerField()
#     reference_number = models.CharField(max_length=20, unique=True)
#     state = models.CharField(max_length=20, choices=LoanState.choices, default=LoanState.PENDING)
#     # docs = models.FileField(upload_to='loan_documents/', null=True, blank=True)
