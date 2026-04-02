"""
URL configuration for Detection_and_Analysis_of_Pill project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from . import views as mv
from Admin import views as av
from Users import views as uv
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),

    #mainView urls
    path('',mv.index,name='index'),
    path('loginForm',mv.loginForm,name='loginForm'),
    path('loginCheck',mv.loginCheck,name='loginCheck'),
    path('userRegisterForm',mv.userRegisterForm,name='userRegisterForm'),

    #adminUrls
    path('adminHome',av.adminHome,name='adminHome'),
    path('userDetails',av.userDetails,name='userDetails'),
    path('activateUser',av.activateUser,name='activateUser'),
    path('adminclassificationView',av.adminclassificationView,name='adminclassificationView'),

    #userurls
    path('userRegister',uv.userRegister,name='userRegister'),
    path('userHome',uv.userHome,name='userHome'),
    path('prediction',uv.prediction,name='prediction'),
    path('classificationView',uv.classificationView,name='classificationView'),


    
    

    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])