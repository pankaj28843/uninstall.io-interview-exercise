"""authserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin

from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)

import auth_app.views as auth_app_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/tokens/auth/', obtain_jwt_token),
    url(r'^api/tokens/refresh/', refresh_jwt_token),
    url(r'^api/tokens/verify/', verify_jwt_token),
    url(r'^api/users/$', auth_app_views.UserList.as_view()),
    url(r'^api/users/(?P<pk>[0-9]+)/$', auth_app_views.UserDetail.as_view()),
]
