from django.urls import path

from . import views

app_name = "bulkop"

urlpatterns = [
    path("", views.bulkop, name="bulkop"),
    path("bulkStart/", views.bulkStart, name="bulkStart"),
    path("bulkForceOff/", views.bulkForceOff, name="bulkForceOff"),
    path("poweron/<int:pk>/", views.poweron, name="poweron"),
    path("forceoff/<int:pk>/", views.forceoff, name="forceoff"),
]