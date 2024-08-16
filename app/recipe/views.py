from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()  # objects that are available to view set
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # overwrite default method to filter recipes of auth user
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        # return correct serializer
        if self.action == "list":
            return serializers.RecipeSerializer
        if self.action == "upload_image":
            return serializers.RecipeImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        # save recipie with authenticated user
        serializer.save(user=self.request.user)

    @action(methods=["POST"], detail=True, url_path="upload-image")  # detail means for just one recipe
    def upload_image(self, request, pk=None):
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)  # get RecipeImageSerializer

        if serializer.is_valid():
            serializer.save()  # save to db
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
