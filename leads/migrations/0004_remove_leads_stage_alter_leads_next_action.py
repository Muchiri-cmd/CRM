# Generated by Django 5.0.7 on 2024-08-06 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0003_leads_stage_alter_leads_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leads',
            name='stage',
        ),
        migrations.AlterField(
            model_name='leads',
            name='next_action',
            field=models.CharField(blank=True, choices=[('New Lead', 'New Lead'), ('Site Visit', 'Site Visit'), ('Design & Proposal', 'Design & Proposal'), ('Submission Proposal', 'Submission Proposal'), ('Meeting', 'Meeting'), ('Won', 'Won'), ('Proposal Update', 'Proposal Update')], max_length=100, null=True),
        ),
    ]