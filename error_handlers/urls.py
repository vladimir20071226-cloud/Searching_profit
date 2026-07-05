from django.urls import path
import error_handlers.views as views
app_name='errors'
urlpatterns=[
    path('error_403/', views.access_denied, name='error_403'),
    path('error_404/', views.page_not_found, name='error_404'),
    path('error_500/', views.something_wrong, name='error_500'),
             ]