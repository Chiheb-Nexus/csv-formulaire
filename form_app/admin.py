from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from form_app import csv_models, account_models

@admin.register(csv_models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('personID', 'personName', 'roleID')

@admin.register(csv_models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('roleID', 'parentRoleID', 'roleName')

@admin.register(account_models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user_pk', 'user_username', 'user_email', 'user_first_name', 
                    'user_last_name', 'user_birthdate')

    def user_pk(self, x):
        if x.user.pk:
            return x.user.pk

    def user_username(self, x):
        if x.user.username:
            return x.user.username

    def user_email(self, x):
        if x.user.email:
            return x.user.email

    def user_last_name(self, x):
        if x.user.last_name:
            return x.user.last_name 

    def user_first_name(self, x):
        if x.user.first_name:
            return x.user.first_name

    def user_birthdate(self, x):
        if x.birth_date:
            return datetime.strftime(x.birth_date, '%d/%m/%Y')

    