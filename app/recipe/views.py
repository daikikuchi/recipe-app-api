from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag

from recipe import serializers


class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """Manage tags in the database"""
    # this requires token authentication is used
    authentication_classes = (TokenAuthentication,)
    # user is authenticated to use the API
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        # Request object should be passed in to self as a class variable
        # user should be assigned to that because authentication is required
        return self.queryset.filter(user=self.request.user).order_by('-name')

    # Override perform_create to assign tag to the correct user
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
