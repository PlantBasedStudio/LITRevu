"""
URL configuration for LITRevu project.

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
from review_app import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.feed, name='feed'),
    path('ticket/create/', views.create_ticket, name='create_ticket'),
    path('review/create/<int:ticket_id>/', views.create_review, name='create_review'),
    path('request_review/', views.request_review, name='request_review'),
    path('tickets', views.tickets, name='tickets'),
    path('tickets/edit/<int:ticket_id>/', views.edit_ticket, name='edit_ticket'), 
    path('tickets/delete/<int:ticket_id>/', views.delete_ticket, name='delete_ticket'),
    path('ticket_review/create/', views.create_ticket_and_review, name='create_ticket_and_review'),
    path('follows/manage/', views.manage_follows, name='manage_follows'),
    path('follows/unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
