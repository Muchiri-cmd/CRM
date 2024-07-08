from django.db import models
from django.contrib.auth.models import User

class Leads(models.Model):
    STATUS_CHOICES = [
        ('Fresh', 'Fresh'),
        ('Site Survey', 'Site Survey'),
        ('Engineering Design', 'Engineering Design'),
        ('Proposal', 'Proposal'),
        ('Commercials Finalized', 'Commercials Finalized'),
        ('PO Received', 'PO Received'),
        ('Cold', 'Cold'),
    ]
    NEXT_ACTION_CHOICES = [
        ('Site Survey', 'Site Survey'),
        ('Engineering Design', 'Engineering Design'),
        ('Proposal', 'Proposal'),
        ('Meeting', 'Meeting'),
        ('Follow-up', 'Follow-up'),
    ]

    SOURCE_CHOICES = [
        ('Online', 'Online'),
        ('Referral', 'Referral'),
        ('Cold Call', 'Cold Call'),
        ('Networking Event', 'Networking Event'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    project_size = models.PositiveIntegerField(null=True, blank=True)
    estimated_project_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    source = models.CharField(max_length=100, choices=SOURCE_CHOICES ,null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leads_as_owner', null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, null=True, blank=True)
    next_action = models.CharField(max_length=100,choices=NEXT_ACTION_CHOICES, null=True, blank=True)
    next_action_scheduled_on = models.DateField(null=True, blank=True)
    next_action_owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Leads'