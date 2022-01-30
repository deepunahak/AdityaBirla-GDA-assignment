"""gda_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('ifsc_search/', views.get_ifsc_details),
    path('statistics/', views.get_log_statistics_details),
    path('bank_leader_board/', views.get_leader_board_details),
    path('api_hit_count/', views.get_api_hit_count),
    path('ifsc_hit_count/', views.get_ifsc_hit_count)
]
