from django.shortcuts import render
from leads.models import Leads
from django.core.paginator import Paginator
import json
from django.db.models import Sum
from django.utils import timezone
import calendar

# Create your views here.
def sales_funnel(request):
    total_leads = Leads.objects.all().count()

    proposals = Leads.objects.filter(status='Proposal').count()
    fresh_leads = Leads.objects.filter(status='Fresh').count()
    project_value = Leads.objects.aggregate(Sum('estimated_project_value'))['estimated_project_value__sum'] or 0

    won = Leads.objects.filter(status='Won').count()
    site_survey = Leads.objects.filter(status='Site Survey').count()

    def calculate_percentage(count):
        return (count / total_leads * 100)

    funnel_data = [
        {"stage": "Fresh", "count": fresh_leads, "percentage": calculate_percentage(fresh_leads)},
        {"stage": "Site Survey", "count": site_survey, "percentage": calculate_percentage(site_survey)},
        {"stage": "Proposals", "count": proposals, "percentage": calculate_percentage(proposals)},
        {"stage": "Won", "count": won, "percentage": calculate_percentage(won)},
        {"stage": "Projects Value", "count": float(project_value), "percentage": calculate_percentage(float(0))}
    ]
    context = {
        'funnel_data': json.dumps(funnel_data)  
    }
    return render(request,'sales/sales_funnel.html',context)

def sales_analytics(request):  
    now = timezone.now()
    current_year = now.year

    labels = [calendar.month_abbr[i] for i in range(1, 13)]
    data = {
        'labels': labels,
        'datasets': []
    }

    statuses = ['Engineering Design', 'Site Survey', 'Proposal', 'Won']
    colors = ['rgba(75, 192, 192, 1)', 'rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)']

  
    for i, status in enumerate(statuses):
        status_data = []
        for month in range(1, 13):
            start_date = timezone.datetime(current_year, month, 1)
            end_date = timezone.datetime(current_year, month, calendar.monthrange(current_year, month)[1], 23, 59, 59)
            count = Leads.objects.filter(status=status, created_at__range=[start_date, end_date]).count()
            status_data.append(count)

        dataset = {
            'label': status,
            'data': status_data,
            'borderColor': colors[i],
            'borderWidth': 1,
            'hidden': i != 0  
        }

        print(count)
        data['datasets'].append(dataset)

    return render(request, 'sales/sales_analytics.html', {'chart_data': data})

def sales_pipeline(request):
    leads = Leads.objects.all()
    paginator_ref = Paginator(leads, 10)
    page_number = request.GET.get('page')
    page_object = paginator_ref.get_page(page_number)


    context = {
        'leads': leads,
        'page_object': page_object
    }   
    print(leads)
    return render(request,'sales/sales_pipeline.html',context)