from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chart.png', views.chart_png, name='chart_png'),
    path('region/<str:region_name>/', views.region_chart, name='region_chart')
]
