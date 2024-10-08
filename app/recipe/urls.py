from django.urls import include, path

from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()
router.register("recipes", views.RecipeViewSet)  # automatically create routes based on RecipeViewSet

app_name = "recipe"

urlpatterns = [
    path("", include(router.urls))  # include routes generated by the router
]