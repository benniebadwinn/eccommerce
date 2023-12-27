"""moontag_project URL Configuration

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
from django.contrib import admin
from django.urls import path , include

from django.views.generic import TemplateView
# from moontag_app.views import ContactView,ReturnPolicyView




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('moontag_app.urls')),
    path('account/',include('account.urls', namespace='login')),
    path('accounts/profile/', TemplateView.as_view(template_name='support.html'),name='support'),
    path('help',TemplateView.as_view(template_name='help.html'),name='help'),
    path('faqs/',TemplateView.as_view(template_name='faqs.html'),name='faqs'),
    # path('contact',ContactView.as_view(),name='contact'),
    # path('return-policy',ReturnPolicyView.as_view(),name='return_policy'),
    path('payment/', include('payment.urls', namespace='payment')),
]
