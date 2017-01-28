# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

from api.models import Account
from api.models import Ticket
from api.models import UserTickets
from serializers import AccountSerializer
from serializers import TicketSerializer
from serializers import UserSerializer
from serializers import UserTicketsSerializer


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
        View class for serialized User model
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
            Allow non-authenticated user to create via POST.
            Other operations allowed only for authenticated users.
        """
        return (AllowAny() if self.request.method == 'POST'
                else IsAuthenticated()),

    def get_queryset(self):
        """
            Filtering records to show only user record.
        """
        #         print User.objects.get(pk=self.request.user.id)
        #         user = self.request.user
        #         return User.objects.filter(pk=user.id)
        #         self.queryset = User.objects.get(pk=self.request.user.id)
        return User.objects.filter(pk=self.request.user.id)  # self.request.user


class TicketViewSet(viewsets.ModelViewSet):
    """
        View for serialized Ticket model
    """
    # show all tickets for authenticated users
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_permissions(self):
        """
            Allow access only for authenticated users.
        """
        return (IsAuthenticated()),


class UserTicketsViewSet(viewsets.ModelViewSet):
    """
        View for serialized UserTickets model
    """
    queryset = UserTickets.objects.all()
    serializer_class = UserTicketsSerializer

    def get_permissions(self):
        """
            Allow access only for authenticated users.
        """
        return (IsAuthenticated()),

    def get_queryset(self):
        """
            Filtering records to show only records which user is owner.
        """
        return UserTickets.objects.filter(user_id=self.request.user)


class AccountViewSet(viewsets.ModelViewSet):
    """
        View for serialized Account model
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_permissions(self):
        """
            Allow access only for authenticated users.
        """
        return (IsAuthenticated()),

    def get_queryset(self):
        """
            Filtering records to show only records which user is owner.
        """
        return Account.objects.filter(user_id=self.request.user)
