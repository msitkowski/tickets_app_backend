# -*- coding: utf-8 -*-
from django.contrib import admin
from api.models import Ticket
from api.models import UserTickets
from api.models import Account
# Register your models here.

admin.site.register(Ticket)
admin.site.register(UserTickets)
admin.site.register(Account)
