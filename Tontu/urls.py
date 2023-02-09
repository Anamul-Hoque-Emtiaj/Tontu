"""Tontu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path,include

urlpatterns = [
    path('jet/', include('jet.urls')),
    path('jet/dashboard/', include('jet.dashboard.urls','jet-dashboard')),
    path('',include('Main.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]

handler404 = 'Main.views.error_404'
# handler500 = 'Main.views.error_500'
handler403 = 'Main.views.error_403'
handler400 = 'Main.views.error_400'
