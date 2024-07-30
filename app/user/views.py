from rest_framework import generics

from user.serializers import UserSerializer


# view to use the user serializer
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
