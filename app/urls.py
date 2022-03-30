from django.shortcuts import redirect
from django.urls import path
from django.views.generic.base import RedirectView
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserResetPasswordForm

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product-detail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('deletecart/', views.delete_cart, name='deletecart'),
    path('buy/', views.buy_now, name='buy-now'),
    
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),

    path('orders/', views.orders, name='orders'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>/', views.mobile, name='mobiledata'),
    path('top-wear/', views.topwear, name='top_wear'),
    path('top-wear/<slug:data>/', views.topwear, name='top_wear'),

    path('registration/', views.UserRegistration.as_view(), name='userregistration'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html', form_class=UserPasswordChangeForm), name='changepassword'),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(template_name='app/changepassworddone.html'), name='password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=UserPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=UserResetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),
    
    path('checkout/', views.checkout, name='checkout'),
    path('payment-done/', views.paymentdone, name='paymentdone'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 
