"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from accounts.views import profile_settings, profile_create, user_create, user_login, user_logout, user_edit, user_delete, confirm_user_delete, profiles_list, like_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", profiles_list),
    path('accounts/<int:pk>/', profile_settings),
    path("accounts/create/", profile_create),
    path("accounts/usercreate/", user_create),
    path("accounts/login/", user_login),
    path("accounts/logout/", user_logout),
    path("accounts/edit/<int:pk>/", user_edit),
    path("accounts/user_delete/<int:pk>/", user_delete),
    path("accounts/confirm_user_delete/<int:pk>/", confirm_user_delete),
    path('accounts/<int:pk>/like/', like_view),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
