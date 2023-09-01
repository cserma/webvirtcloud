from django.urls import path

from . import views

urlpatterns = [
    path("", views.bulkop, name="bulkop"),
    path("bulkStart/", views.bulkStart, name="bulkStart"),
    path("bulkForceOff/", views.bulkForceOff, name="bulkForceOff"),
]