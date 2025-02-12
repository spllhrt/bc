from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),  
    path('dashboard/', views.dashboard, name='dashboard'), 
    # path('profile/', views.update_profile, name='profile'),  # Uncomment and define if needed
    path('logout/', views.logout_user, name='logout'),
    path('users/', views.users, name='users'),
    path('reports/', views.reports, name='reports'),
    # path('blank/', views.blank, name='blank'),  # Uncomment and define if needed
    path('google-auth/', views.google_auth, name='google-auth'),  # Add trailing slash for consistency
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)