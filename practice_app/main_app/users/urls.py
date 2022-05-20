from django.urls import path, include
from .views import *


urlpatterns = [
    path('user/<username>', ProfileDetailView.as_view(), name='user-page'),
    path('edit-profile/', ProfileEditView.as_view(), name='profile-edit'),
    path('edit-profile-api/', edit_profile, name='profile-edit-api'),
    path('all-profiles/', get_all_profiles, name='all-profile-api'),
]