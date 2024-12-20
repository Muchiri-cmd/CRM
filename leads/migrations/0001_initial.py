# Generated by Django 5.0.7 on 2024-08-03 11:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Leads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('company', models.CharField(max_length=100)),
                ('industry', models.CharField(blank=True, choices=[('Agriculture', 'Agriculture'), ('Automobile', 'Automobile'), ('Banking', 'Banking'), ('Construction', 'Construction'), ('Energy', 'Energy'), ('Food', 'Food'), ('Healthcare', 'Healthcare'), ('Hospitality', 'Hospitality'), ('IT', 'IT'), ('Manufacturing', 'Manufacturing'), ('Real Estate', 'Real Estate'), ('Retail', 'Retail'), ('Telecom', 'Telecom'), ('Transportation', 'Transportation'), ('Other', 'Other')], max_length=100, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('country', models.CharField(blank=True, choices=[('Algeria', 'Algeria'), ('Angola', 'Angola'), ('Benin', 'Benin'), ('Botswana', 'Botswana'), ('Burkina Faso', 'Burkina Faso'), ('Burundi', 'Burundi'), ('Cabo Verde', 'Cabo Verde'), ('Cameroon', 'Cameroon'), ('Central African Republic', 'Central African Republic'), ('Chad', 'Chad'), ('Comoros', 'Comoros'), ('Congo', 'Congo'), ('Djibouti', 'Djibouti'), ('Egypt', 'Egypt'), ('Equatorial Guinea', 'Equatorial Guinea'), ('Eritrea', 'Eritrea'), ('Eswatini', 'Eswatini'), ('Ethiopia', 'Ethiopia'), ('Gabon', 'Gabon'), ('Gambia', 'Gambia'), ('Ghana', 'Ghana'), ('Guinea', 'Guinea'), ('Guinea-Bissau', 'Guinea-Bissau'), ('Ivory Coast', 'Ivory Coast'), ('Kenya', 'Kenya'), ('Lesotho', 'Lesotho'), ('Liberia', 'Liberia'), ('Libya', 'Libya'), ('Madagascar', 'Madagascar'), ('Malawi', 'Malawi'), ('Mali', 'Mali'), ('Mauritania', 'Mauritania'), ('Mauritius', 'Mauritius'), ('Morocco', 'Morocco'), ('Mozambique', 'Mozambique'), ('Namibia', 'Namibia'), ('Niger', 'Niger'), ('Nigeria', 'Nigeria'), ('Rwanda', 'Rwanda'), ('Sao Tome and Principe', 'Sao Tome and Principe'), ('Senegal', 'Senegal'), ('Seychelles', 'Seychelles'), ('Sierra Leone', 'Sierra Leone'), ('Somalia', 'Somalia'), ('South Africa', 'South Africa'), ('South Sudan', 'South Sudan'), ('Sudan', 'Sudan'), ('Tanzania', 'Tanzania'), ('Togo', 'Togo'), ('Tunisia', 'Tunisia'), ('Uganda', 'Uganda'), ('Zambia', 'Zambia'), ('Zimbabwe', 'Zimbabwe')], max_length=100, null=True)),
                ('address', models.CharField(max_length=200)),
                ('project_type', models.CharField(blank=True, choices=[('EPC', 'EPC'), ('ETA', 'ETA'), ('PPA', 'PPA'), ('EPC & PPA', 'EPC & PPA'), ('EPC & LEASE', 'EPC & LEASE'), ('PPA & LEASE', 'PPA & LEASE'), ('EPC & PPA & LEASE', 'EPC & PPA & LEASE'), ('Lease', 'Lease')], max_length=100, null=True)),
                ('project_size', models.PositiveIntegerField(blank=True, null=True)),
                ('bess_size', models.PositiveIntegerField(blank=True, null=True)),
                ('estimated_project_value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('source', models.CharField(blank=True, choices=[('Tender', 'Tender'), ('Internal', 'Internal'), ('Channel Partner', 'Channel Patner'), ('Organic', 'Organic')], max_length=100, null=True)),
                ('status', models.CharField(blank=True, choices=[('Fresh', 'Fresh'), ('Site Survey', 'Site Survey'), ('Engineering Design', 'Engineering Design'), ('Proposal', 'Proposal'), ('Commercials Finalized', 'Commercials Finalized'), ('PO Received', 'PO Received'), ('Cold', 'Cold'), ('Won', 'Won')], max_length=100, null=True)),
                ('next_action', models.CharField(blank=True, choices=[('Site Survey', 'Site Survey'), ('Engineering Design', 'Engineering Design'), ('Proposal', 'Proposal'), ('Meeting', 'Meeting'), ('Follow-up', 'Follow-up')], max_length=100, null=True)),
                ('next_action_scheduled_on', models.DateField(blank=True, null=True)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leads_as_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Leads',
            },
        ),
    ]
