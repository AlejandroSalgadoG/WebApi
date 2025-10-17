from django.urls import include, path
from rest_framework.routers import DefaultRouter

from summary import views

router = DefaultRouter()
router.register("summary", views.SummaryViewSet)

app_name = "summary"

urlpatterns = [
    path("", include(router.urls)),
]
