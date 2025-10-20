from rest_framework import viewsets, generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from app.models import Info, Task
from app.process import process_task
from app.serializers import DateRangeSerializer, InfoSerializer, TaskSerializer


class InfoViewSet(viewsets.ModelViewSet):
    serializer_class = InfoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Info.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(
    request=DateRangeSerializer,
    responses={
        201: {
            'type': 'object',
            'properties': {
                'id': {
                    'type': 'string',
                    'format': 'uuid',
                    'description': 'Task ID for tracking the asynchronous processing'
                }
            },
            'description': 'Returns only the task ID'
        }
    },
    summary='Create task',
    description='Creates an asynchronous task to process info within a date range. Returns only the task ID for tracking the processing status.',
)
class TaskCreateView(generics.CreateAPIView):
    serializer_class = DateRangeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = DateRangeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Invalid execution parameters', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        task = Task.objects.create(
            user=request.user,
            task_type='process',
        )

        # Start processing task (in a real implementation, this would be queued)
        import threading
        thread = threading.Thread(target=process_task, args=(task.id, serializer.validated_data))
        thread.daemon = True
        thread.start()

        return Response({"id": str(task.id)}, status=status.HTTP_201_CREATED)


class TaskStatusView(generics.RetrieveAPIView):
    serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
