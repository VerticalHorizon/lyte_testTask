"""lyte_test_task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.http import JsonResponse
from django.urls import include, path
from django.contrib.staticfiles.urls import urlpatterns as static_urlpatterns
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/signin/', obtain_jwt_token, name='create-token'),
    path('api/refresh/', refresh_jwt_token, name='refresh-token'),
    path('api/verify/', verify_jwt_token, name='verify-token'),
    path('api/events/', include('events.urls')),
    path('', lambda request: JsonResponse({'status': 'OK'})),
]

urlpatterns += static_urlpatterns
