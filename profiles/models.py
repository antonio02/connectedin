from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_of_birth   = models.DateField(null=False, blank=False)
    contacts        = models.ManyToManyField('Profile')
    blocked_contacts= models.ManyToManyField('Profile', related_name='%(class)s_blocked_contacts')

class Invitation(models.Model):
    sender      = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_invitations' )
    receiver    = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_invitations')

    def accept(self):
        self.sender.contacts.add(self.receiver)
        self.receiver.contacts.add(self.sender)
        self.delete()

    def decline(self):
        self.delete()

    def cancel(self):
        self.delete()
