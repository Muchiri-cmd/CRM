from django.shortcuts import render
from leads.models import Leads
from django.core.paginator import Paginator
import json
from django.db.models import Sum
from django.utils import timezone
import calendar
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def sales_funnel(request):
    if request.user.is_employee:
        leads = Leads.objects.filter(Q(owner=request.user) | Q(next_action_owner=request.user))
    else:
        leads = Leads.objects.all()

    total_leads = leads.count()

    fresh_leads = leads.filter(status='Fresh').count()
    project_value = leads.aggregate(Sum('estimated_project_value'))['estimated_project_value__sum'] or 0
    won = leads.filter(status='Won').count()
    cold = leads.filter(status='Cold').count()
    neutral = leads.filter(status='Neutral').count()
    warm = leads.filter(status='Warm').count()

    def calculate_percentage(count):
        return (count / total_leads * 100) if total_leads > 0 else 0

    funnel_data = [
        {"stage": "Fresh", "count": fresh_leads, "percentage": calculate_percentage(fresh_leads)},
        {"stage": "Cold", "count": cold, "percentage": calculate_percentage(cold)},
        {"stage": "Warm", "count": warm, "percentage": calculate_percentage(warm)},
        {"stage": "Neutral", "count": neutral, "percentage": calculate_percentage(neutral)},
        {"stage": "Won", "count": won, "percentage": calculate_percentage(won)},
        {"stage": "Projects Value", "count": float(project_value), "percentage": 0} 
    ]

    context = {
        'funnel_data': json.dumps(funnel_data)  
    }

    if request.user.is_employee:
        return render(request, 'sales/user_funnel.html', context)
    elif request.user.is_manager:
        return render(request, 'sales/sales_funnel.html', context)
    else:
        return render(request, 'dashboard/no_access.html')

def sales_analytics(request):
    if request.user.is_employee:
        leads = Leads.objects.filter(Q(owner=request.user) | Q(next_action_owner=request.user))
    else:
        leads = Leads.objects.all()

    now = timezone.now()
    current_year = now.year

    labels = [calendar.month_abbr[i] for i in range(1, 13)]
    data = {
        'labels': labels,
        'datasets': []
    }

    stages = ['New Lead', 'Site Visit', 'Design & Proposal', 'Submission Proposal', 'Meeting', 'Proposal Update']
    colors = ['rgba(75, 192, 192, 1)', 'rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)', 'rgba(153, 102, 255, 1)', 'rgba(255, 159, 64, 1)']

    for i, status in enumerate(stages):
        status_data = []
        for month in range(1, 13):
            start_date = timezone.make_aware(timezone.datetime(current_year, month, 1))
            end_date = timezone.make_aware(timezone.datetime(current_year, month, calendar.monthrange(current_year, month)[1], 23, 59, 59))
            count = leads.filter(next_action=status, created_at__range=[start_date, end_date]).count()
            status_data.append(count)

        dataset = {
            'label': status,
            'data': status_data,
            'borderColor': colors[i % len(colors)],  # Use modulo to avoid index error if stages > colors
            'borderWidth': 1,
            'hidden': i != 0  # Optionally adjust visibility
        }

        data['datasets'].append(dataset)

    if request.user.is_employee:
        return render(request, 'sales/user_analytics.html', {'chart_data': data})
    elif request.user.is_manager:
        return render(request, 'sales/sales_analytics.html', {'chart_data': data})
    else:
        return render(request, 'dashboard/no_access.html')

@login_required
def sales_pipeline(request):
    if request.user.is_employee:
        leads = Leads.objects.filter(Q(owner=request.user) | Q(next_action_owner=request.user))
    else:
        leads = Leads.objects.all()

    paginator_ref = Paginator(leads, 10)
    page_number = request.GET.get('page')
    page_object = paginator_ref.get_page(page_number)

    context = {
        'leads': leads,
        'page_object': page_object
    }

    if request.user.is_employee:
        return render(request, 'sales/user_pipeline.html', context)
    elif request.user.is_manager:
        return render(request, 'sales/sales_pipeline.html', context)
    else:
        return render(request, 'dashboard/no_access.html')