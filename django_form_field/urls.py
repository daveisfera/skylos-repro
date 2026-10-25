from django.urls import path

from django_form_field.views import join_facility

urlpatterns = [
    path("join/", join_facility, name="join_facility"),
]
