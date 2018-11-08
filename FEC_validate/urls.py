"""FEC_validate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_nested import routers
from django.views.decorators.csrf import csrf_exempt
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='FEC-Validate API')


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^admin$', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/', include('FECvalidate.urls')),
    
    #url(r'^api/v1/auth/login$', csrf_exempt(LoginView.as_view()), name='login'),
    #url(r'^api/v1/auth/login$', LoginView.as_view(), name='login'),
    #url(r'^api/v1/auth/logout/$', LogoutView.as_view(), name='logout'),
    #url(r'^api/docs/', include('rest_framework_swagger.urls')),
    url(r'^api/docs$', schema_view),
    url(r'^api/v1/token/obtain$', obtain_jwt_token),
    url(r'^api/v1/token/refresh$', refresh_jwt_token),
    #url('^.*$', IndexView.as_view(), name='index'),
]



