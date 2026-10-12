from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
        path('holo-lab/', views.holo_lab, name='holo_lab'),
        path('holo-bg-2.jpg', views.holocloth_asset, {'asset_name': 'holo-bg-2.jpg'}, name='holocloth_cloth_image'),
        path('bump-scratches.jpg', views.holocloth_asset, {'asset_name': 'bump-scratches.jpg'}, name='holocloth_bump_image'),
    path('events/', views.events_list, name='events_list'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/register/', views.register_for_event, name='register_for_event'),
    path('event/<int:event_id>/cancel/', views.cancel_registration, name='cancel_registration'),
    path('request-event/', views.request_event, name='request_event'),
    path('organizer/', views.organizer_dashboard, name='organizer_dashboard'),
    path('organizer/create/', views.create_event, name='create_event'),
    path('organizer/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('organizer/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('organizer/event/<int:event_id>/analytics/', views.event_analytics, name='event_analytics'),
    path('organizer/event/<int:event_id>/certificates/', views.manage_event_certificates, name='manage_event_certificates'),
    path('organizer/request/<int:event_request_id>/<str:action>/', views.update_event_request, name='update_event_request'),
    path('certificate/<int:certificate_id>/download/', views.download_certificate, name='download_certificate'),
    path('profile/', views.profile, name='profile'),
]
