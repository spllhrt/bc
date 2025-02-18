from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),  
    path('dashboard/', views.dashboard, name='dashboard'), 
    # path('profile/', views.update_profile, name='profile'), 
    path('logout/', views.logout_user, name='logout'),
    path('users/', views.users, name='users'),
    path('reports/', views.reports, name='reports'),
    # path('blank/', views.blank, name='blank'),  
    path('google-auth/', views.google_auth, name='google-auth'),  
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('charts/', views.charts, name='charts'),
    
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('features/', views.features, name='features'),
    path('', views.index, name='index'),
    path('services/', views.services, name='services'),
    
    path('profile/', views.profile, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)