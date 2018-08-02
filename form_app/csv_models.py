from django.db import models
from django.utils.translation import ugettext_lazy as _


class Role(models.Model):
    '''Role DB model'''
    roleID          = models.AutoField(primary_key=True, verbose_name=_('Role ID'),
                        blank=False, null=False)
    parentRoleID    = models.ForeignKey(
                        'self', to_field='roleID', verbose_name=_('Parent Role ID'), 
                        blank=True, null=True, related_name='prid', on_delete=models.CASCADE)
    roleName        = models.CharField(max_length=255, verbose_name=_('Role Name'))

    def __str__(self):
        return '{0} - {1}'.format(self.roleID, self.roleName)
    

class Person(models.Model):
    '''Person DB model'''
    personID    = models.AutoField(primary_key=True, verbose_name=_('Person ID'), 
                    blank=False, null=False)
    personName  = models.CharField(max_length=255, verbose_name=_('Person Name'), 
                    blank=False, null=False)
    roleID      = models.ForeignKey(
                    Role, verbose_name=_('Role ID'), db_column='roleID_roleID', related_name='rid', 
                    blank=False, null=False,on_delete=models.CASCADE)

    def __str__(self):
        return self.personName
