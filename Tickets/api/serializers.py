# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone
from api.models import Ticket, Account
from api.models import UserTickets
from dateutil.relativedelta import relativedelta


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username',
                  'password', 'first_name',
                  'last_name', 'email')
        write_only_fields = ('password',)
        read_only_fields = ('is_staff',
                            'is_superuser', 'is_active',
                            'date_joined',)

    def create(self, validated_data):
        user = User(username=validated_data.get('username'),
                    first_name=validated_data.get('first_name'),
                    last_name=validated_data.get('last_name'),
                    email=validated_data.get('email'))
        user.set_password(validated_data.get('password'))
        user.save()
        account = Account(user_id=user)
        account.save()
        #         validated_data.update({'password': })
        return user  # serializers.ModelSerializer.create(self, validated_data)

    def update(self, instance, validated_data):
        # hash password if updated
        if validated_data.get('password', None):
            validated_data['password'] = instance.set_password(validated_data.get('password'))

        return serializers.ModelSerializer.update(self, instance, validated_data)


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('url', 'name',
                  'price', 'description',
                  'time_of_validity', 'time_unit')
        read_only_fields = ('url', 'name',
                            'price', 'description',
                            'time_of_validity', 'time_unit')


class UserTicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTickets
        fields = ('url', 'user_id',
                  'ticket_id', 'status',
                  'valid_to_date')
        read_only_fields = ('url', 'user_id',
                            'valid_to_date')

    def create(self, validated_data):
        # set default status to new 
        # even if user try to create ticket with other status
        validated_data['status'] = 'new'
        # set current user as ticket buyer
        validated_data['user_id'] = self.context.get('request').user
        # getting current user account from which money will be subtracted
        account = Account.objects.get(user_id=validated_data.get('user_id').id)
        # get ticket
        ticket = Ticket.objects.get(pk=validated_data.get('ticket_id').id)
        # subtract money from user account if enough money
        if account.account_balance >= ticket.price:
            account.account_balance -= ticket.price
            account.save()

        else:
            raise serializers.ValidationError(detail='Not enough money! Please charge your account.')

        return serializers.ModelSerializer.create(self, validated_data)

    def update(self, instance, validated_data):
        # update only new and active tickets
        if instance.status != 'inactive' \
                and validated_data.get('status') != 'new' \
                and instance.status != validated_data.get('status'):
            # when ticket change state from zakupiony to skasowany, set valid to date
            if instance.status == 'new' and validated_data.get('status') == 'active':
                # set ticket valid to date depending on ticket time unit and validity
                if instance.ticket_id.time_unit == 'm':
                    instance.valid_to_date = timezone.now() + relativedelta(
                        seconds=+instance.ticket_id.time_of_validity * 60)

                else:
                    instance.valid_to_date = timezone.now() + relativedelta(hours=+instance.ticket_id.time_of_validity)

            # update only status and valid to date
            if instance.valid_to_date > timezone.now():
                instance.status = validated_data.get('status')

            else:
                instance.status = 'inactive'

            instance.save()

        return instance


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('url', 'user_id',
                  'account_balance',)
        read_only_fields = ('url', 'user_id',)

    def update(self, instance, validated_data):
        if validated_data.get('account_balance', None) and validated_data.get('account_balance') > 0:
            validated_data['account_balance'] += instance.account_balance

        else:
            raise serializers.ValidationError(detail='Account balance must be positive non 0 value!')

        return serializers.ModelSerializer.update(self, instance, validated_data)
