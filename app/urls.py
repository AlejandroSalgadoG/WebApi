from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app import views


app_name = 'app'

router = DefaultRouter()
router.register("info", views.InfoViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('task/', views.TaskCreateView.as_view(), name='task'),
    path('task/<uuid:id>', views.TaskStatusView.as_view(), name='task_status'),
    path('queue/', views.QueueStatusView.as_view(), name='queue'),
]
