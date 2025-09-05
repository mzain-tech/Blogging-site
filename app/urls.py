from django.urls import path
from . import views

urlpatterns=[
    path('', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('dashboard_redirect/', views.dashboard_redirect, name='dashboard_redirect'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock_user/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path('approved_blog/<int:blog_id>/', views.approved_blog, name='approved_blog'),
    path('rejected_blog/<int:blog_id>/', views.reject_blog, name='reject_blog'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('add_blog/', views.add_blog, name='add_blog'),
    path('edit_blog/<int:id>/', views.edit_blog, name='edit_blog'),
    path('del_blog/<int:id>/', views.del_blog, name='del_blog'),
    path('home/', views.home, name='home'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('blog_detail/<int:id>/',views.blog_detail, name='blog_detail'),
    path('del_comment/<int:id>/', views.del_comment, name='del_comment'),
    path('analytics/', views.analytics, name='analytics'),
    path('del_user/<int:user_id>/', views.del_user, name='del_user'),
]