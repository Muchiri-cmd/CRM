from django.db import models
# from django.contrib.auth.models import User
from main.settings import AUTH_USER_MODEL as User

class Leads(models.Model):
    STATUS_CHOICES = [
        ('Neutral', 'Neutral'),
        ('Warm', 'Warm'),
        ('Won', 'Won'),
    ]

    STAGES = [
        ('New Lead', 'New Lead'),
        ('Site Visit', 'Site Visit'),
        ('Design & Proposal', 'Design & Proposal'),
        ('Submission Proposal', 'Submission Proposal'),
        ('Update', 'Update'),
        ('Meeting', 'Meeting'),
        ('Won', 'Won'),
        ('Proposal Update', 'Proposal Update'),
    ]
    NEXT_ACTION_CHOICES = [
        ('Site Survey', 'Site Survey'),
        ('Engineering Design', 'Engineering Design'),
        ('Proposal', 'Proposal'),
        ('Meeting', 'Meeting'),
        ('Follow-up', 'Follow-up'),
    ]

    SOURCE_CHOICES = [
        ('Tender', 'Tender'),
        ('Internal', 'Internal'),
        ('Channel Partner', 'Channel Patner'),
        ('Organic', 'Organic'),
    ]

    PROJECT_TYPES = [
        ('EPC','EPC'),
        ('ETA', 'ETA'),
        ('PPA', 'PPA'),
        ('EPC & PPA', 'EPC & PPA'),
        ('EPC & LEASE', 'EPC & LEASE'),
        ('PPA & LEASE', 'PPA & LEASE'),
        ('EPC & PPA & LEASE', 'EPC & PPA & LEASE'),
        ('Lease','Lease')
    ]

    INDUSTRY = [
        ('Agriculture','Agriculture'),
        ('Automobile','Automobile'),
        ('Banking','Banking'),
        ('Construction','Construction'),
        ('Energy','Energy'),
        ('Food','Food'),
        ('Healthcare','Healthcare'),
        ('Hospitality','Hospitality'),
        ('IT','IT'),
        ('Manufacturing','Manufacturing'),
        ('Real Estate','Real Estate'),
        ('Retail','Retail'),
        ('Telecom','Telecom'),
        ('Transportation','Transportation'),
        ('Other','Other')
    ]

    COUNTRIES = [
        ('Algeria', 'Algeria'),
        ('Angola', 'Angola'),
        ('Benin', 'Benin'),
        ('Botswana', 'Botswana'),
        ('Burkina Faso', 'Burkina Faso'),
        ('Burundi', 'Burundi'),
        ('Cabo Verde', 'Cabo Verde'),
        ('Cameroon', 'Cameroon'),
        ('Central African Republic', 'Central African Republic'),
        ('Chad', 'Chad'),
        ('Comoros', 'Comoros'),
        ('Congo', 'Congo'),
        ('Djibouti', 'Djibouti'),
        ('Egypt', 'Egypt'),
        ('Equatorial Guinea', 'Equatorial Guinea'),
        ('Eritrea', 'Eritrea'),
        ('Eswatini', 'Eswatini'),
        ('Ethiopia', 'Ethiopia'),
        ('Gabon', 'Gabon'),
        ('Gambia', 'Gambia'),
        ('Ghana', 'Ghana'),
        ('Guinea', 'Guinea'),
        ('Guinea-Bissau', 'Guinea-Bissau'),
        ('Ivory Coast', 'Ivory Coast'),
        ('Kenya', 'Kenya'),
        ('Lesotho', 'Lesotho'),
        ('Liberia', 'Liberia'),
        ('Libya', 'Libya'),
        ('Madagascar', 'Madagascar'),
        ('Malawi', 'Malawi'),
        ('Mali', 'Mali'),
        ('Mauritania', 'Mauritania'),
        ('Mauritius', 'Mauritius'),
        ('Morocco', 'Morocco'),
        ('Mozambique', 'Mozambique'),
        ('Namibia', 'Namibia'),
        ('Niger', 'Niger'),
        ('Nigeria', 'Nigeria'),
        ('Rwanda', 'Rwanda'),
        ('Sao Tome and Principe', 'Sao Tome and Principe'),
        ('Senegal', 'Senegal'),
        ('Seychelles', 'Seychelles'),
        ('Sierra Leone', 'Sierra Leone'),
        ('Somalia', 'Somalia'),
        ('South Africa', 'South Africa'),
        ('South Sudan', 'South Sudan'),
        ('Sudan', 'Sudan'),
        ('Tanzania', 'Tanzania'),
        ('Togo', 'Togo'),
        ('Tunisia', 'Tunisia'),
        ('Uganda', 'Uganda'),
        ('Zambia', 'Zambia'),
        ('Zimbabwe', 'Zimbabwe'),
    ]

    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    industry = models.CharField(max_length=100, null=True, choices=INDUSTRY, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=100, choices=COUNTRIES , null=True, blank=True)
    address = models.CharField(max_length=200)
    project_type = models.CharField(max_length=100,choices=PROJECT_TYPES,null=True,blank=True)
    project_size = models.PositiveIntegerField(null=True, blank=True)
    bess_size = models.PositiveIntegerField(null=True, blank=True)
    estimated_project_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    source = models.CharField(max_length=100, choices=SOURCE_CHOICES ,null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leads_as_owner', null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, null=True, blank=True)
    stage = models.CharField(max_length=100, choices=STAGES, null=True, blank=True)
    next_action = models.CharField(max_length=100,choices=NEXT_ACTION_CHOICES, null=True, blank=True)
    next_action_scheduled_on = models.DateField(null=True, blank=True)
    next_action_owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Leads'