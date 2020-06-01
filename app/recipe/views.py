from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe

from recipe import serializers


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """Base viewset for user owned recipe attributes"""
    # this requires token authentication is used
    authentication_classes = (TokenAuthentication,)
    # user is authenticated to use the API
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        # Request object should be passed in to self as a class variable
        # user should be assigned to that because authentication is required
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new object """
        # Override perform_create to assign tag to the correct user
        # Called by CreateModelMixin when saving a new object instance.
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""
    # Only code unique to this class is here thanks to inheritance
    # of BaseRecipeAttrViewSet
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""
        return self.queryset.filter(user=self.request.user)

    # to retrive the serializer class for a particular request
    # ViewSet a number of actions available, list returns default
    #  if action is retrieve, return the detail serializer
    def get_serializer_class(self):
        """Return appropriate serializer class"""
        # action being used for our current request
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer

        return self.serializer_class
