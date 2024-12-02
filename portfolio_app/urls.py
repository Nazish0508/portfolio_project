from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('choose_template/', views.choose_template, name='choose_template'),
    # path('create_portfolio/<str:template>/', views.create_portfolio, name='create_portfolio'),
    # path('edit_portfolio/<int:portfolio_id>/', views.edit_portfolio, name='edit_portfolio'),
    # path('view_portfolio/<int:portfolio_id>/', views.view_portfolio, name='view_portfolio'),
     path('edit-portfolio/', views.edit_portfolio, name='edit_portfolio'),
    path('create_portfolio/', views.create_portfolio, name='create_portfolio'),

    path('view-portfolio/', views.view_portfolio, name='view_portfolio'),
    #public view ki url
    path('portfolio/<int:user_id>/', views.public_portfolio_view, name='public_portfolio'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]