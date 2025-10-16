from django.urls import path
from user import views


app_name = "user"  # used in reverse function


urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"),
]
