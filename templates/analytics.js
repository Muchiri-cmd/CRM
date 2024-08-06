{% load static %}
{% block stylesheets %}
    <link rel="stylesheet" href="{% static 'css/sales_analytics.css' %}">
{% endblock %}

<canvas id="myChart"></canvas>
{{ chart_data|json_script:"chartData" }}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="{% static 'js/analytics.js' %}"></script>