from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('signup', views.SignupView.as_view(), name='signup'),
    path('signin', views.SigninView.as_view(), name='signin'),
    path('signout', views.SignoutView.as_view(), name='signout'),
    path('dashboard', views.DashboardView.as_view(), name='dashboard'),
    path('thankyou', views.ThankyouView.as_view(), name='thankyou'),
    path('mydata', views.MyDataView.as_view(), name='mydata')
]