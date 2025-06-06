from django.urls import path
from . import views

#Custom Error Pages Routes
handler400 = 'webcore.views.handler400'
handler403 = 'webcore.views.handler403'
handler404 = 'webcore.views.handler404'
handler500 = 'webcore.views.handler500'

app_name = 'webcore'
urlpatterns = [

	#Default Pages Routes
	path('',  views.HomePageView.as_view(), name='home-page'),
	path('aboutus/', views.AboutUsPageView.as_view(), name = 'about-us'),
	path('contactus/', views.ContactUsPageView.as_view(), name = 'contact-us'),
	
	
	# #Email Campaign
	# path('subscribe/', views.AddEmailVerification.as_view(), name = 'verify-email-form'),
	# path('subscribe/verify/<str:verification_key>/', views.CheckEmailVerification.as_view(), name = 'verify-email-status'),
	# path('subscribe/<int:subscriber_id>/add/<int:campaign_list>/', views.UpdateNewsletterSubscription.as_view(), name = 'add-to-campaign'),
	# path('unsubscribe/<int:subscriber_id>/add/<int:campaign_list>/', views.UpdateNewsletterSubscription.as_view(), name = 'remove-from-campaign'),	#Banner

	
	#Category
	path('category/', views.CategoryListView.as_view(), name="webcore-category-List"),
	path('category/add/', views.CategoryCreateView.as_view(), name="webcore-category-create"),
	path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name="webcore-category-detail"),
	path('category/<slug:slug>/edit/', views.CategoryUpdateView.as_view(), name="webcore-category-edit"),
	path('category/<slug:slug>/delete/', views.CategoryDeleteView.as_view(), name="webcore-category-delete"),
	path('categpry/<int:pk>/', views.CategoryDetailView.as_view(), name ="webcore-category-pk"),	
	path('check_user_exists/', views.UserCheckView.as_view(), name ="webcore-user-check"),

	#Pages
	# path('create_page/', views.PageCreateView.as_view(), name="webcore-page-create"),
	# path('<slug:slug>/', views.PageDetailView.as_view(), name="webcore-page-detail"),
	# path('<slug:slug>/edit/', views.PageUpdateView.as_view(), name="webcore-page-edit"),
	# path('<slug:slug>/delete/', views.PageDeleteView.as_view(), name="webcore-page-delete"),
	# path('<int:pk>/', views.PageDetailView.as_view(), name ="webcore-page-pk"),



	#Tag

#Default Apps Routes

]