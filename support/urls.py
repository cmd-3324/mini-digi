from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('tickets/<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('tickets/create/', views.create_ticket, name='create_ticket'),
]