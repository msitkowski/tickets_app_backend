# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
 
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
 
# for user in User.objects.all():
#     Token.objects.get_or_create(user=user)
 
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    '''
        Method called every time when new user is created
        and generate auth token.
    '''
    if created:
        Token.objects.create(user=instance)
        
# application classes
class Ticket(models.Model):
    '''
        Model store tickets
    '''
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(max_length=100)
    time_of_validity = models.IntegerField()
    time_unit = models.CharField(max_length=1, choices=(('m', 'Min'),
                                                        ('h', 'Godz')),
                                 default='m')
    
    def __unicode__(self):
        return '%s %d %s'%(self.name, self.time_of_validity,
                           self.time_unit)
    
class Account(models.Model):
    '''
       Model store user account balance 
    '''
    account_balance = models.DecimalField(max_digits=6, decimal_places=2,
                                          default=0.00, validators=[MinValueValidator(Decimal('0.00'))])
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __unicode__(self):
        return '%s %0.2f PLN'%(self.user_id.username, self.account_balance)
    
class UserTickets(models.Model):
    '''
        Model store tickets bought by user
    '''
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket_id = models.ForeignKey(Ticket, null=True,
                                  on_delete=models.SET_NULL)
    status = models.CharField(max_length=10,
                              choices=(('new', 'Zakupiony'),
                                       ('active', 'Skasowany'),
                                       ('inactive', 'Nieważny')),
                              default='new')
    valid_to_date = models.DateTimeField(blank=True, null=True)
    
    def __unicode__(self):
        return '[%s] %s %s %s'%(self.status, self.ticket_id.name,
                                self.ticket_id.time_of_validity,
                                self.ticket_id.time_unit)