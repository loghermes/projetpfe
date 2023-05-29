from django.urls import path
from  authh2o import views
urlpatterns = [
    path('Signup/',views.Signup,name='Signup'),
    path('Login/',views.handlelogin,name='handlelogin'),
    path('Logout/',views.handlelogout,name='handlelogout'),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),
    path('request-reset-email/',views.RequestResetEmailView.as_view(),name='request-reset-email'),
    path('set-new-password/<uidb64>/<token>',views.SetNewPasswordView.as_view(),name='set-new-password'),
    path('update_user/',views.update_user,name='update_user'),
    
]
