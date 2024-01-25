from django.urls import path
from . import views

urlpatterns = [
    path('bodiweb_request/', views.bodiweb, name='bodiweb'),
    # path('login/', views.login_user, name='login'),
    # path('logout/', views.logout_user, name='logout')
]