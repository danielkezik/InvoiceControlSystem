from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'register/', views.register, name='register'),
    path(r'login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path(r'logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path(r'balance/', views.AddBalance.as_view(), name='add_balance'),
    path(r'new_invoice/', views.NewInvoice.as_view(), name='new_invoice'),
    path(r'my_clients/', views.ClientsList.as_view(), name='clients_list'),
    path(r'invoice/<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice_detail'),
]
