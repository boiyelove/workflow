from django.conf.urls import url
from . import views


app_name="accounts"

urlpatterns = [
	url(r'^login/$', views.LoginView.as_view(), name="login"),
	url(r'^logout/$', views.LogoutView.as_view(), name="logout"),
	url(r'^register/$', views.RegisterView.as_view(), name='register'),
	url(r'^ref/(?P<username>[\w-]+)/$', views.GetRef.as_view(), name='get-referral'),
	url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
	url(r'^profile/$', views.UserProfileView.as_view(), name='userprofile'),
	url(r'^profile/payment/$', views.DonateMethodListView.as_view(), name='donatemethod-list'),
	url(r'^profile/payment/new/$', views.DonateMethodCreateView.as_view(), name="donatemethod-create"),
	url(r'^profile/payment/(?P<pk>\d+)/edit/$', views.DonateMethodUpdateView.as_view(), name='donatemethod-edit'),
	url(r'^profile/payment/(?P<pk>\d+)/delete/$', views.DonateMethodDeleteView.as_view(), name='donatemethod-delete'),
	url(r'^verify_email/(?P<verification_key>[\w-]+)/$', views.EmailVerificationView.as_view(), name='verify-email'),
	url(r'^request_new_password/$', views.PasswordChangeRequestView.as_view(), name='password-request'),
	url(r'^change_password/$', views.PasswordChangeView.as_view(), name='password-change'),
]