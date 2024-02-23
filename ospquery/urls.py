from django.urls import path
from . import views

urlpatterns = [
    path('osp_status/', views.osp_status, name='osp_status'),
    # path('login/', views.login_user, name='login'),
    # path('logout/', views.logout_user, name='logout')
]