from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
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
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()

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

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of intergers"""
        # our_string = '1,2,3'
        # our_string_list = [1,2,3]
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""
        # retrieve get parameters, query params is dictionary
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        # we do this not reassign our queryset
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            # First underscore is Django syntax for filtering on foreignKey
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(user=self.request.user)

    # to retrive the serializer class for a particular request
    # ViewSet a number of actions available, list returns default
    #  if action is retrieve, return detail serializer, instead of default one
    def get_serializer_class(self):
        """Return appropriate serializer class"""
        # action being used for our current request
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    # Assigns the user of the created recipe to current autheticated user.
    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)

    # Above functions are default ones that overrode.
    # By using @action, we can create custom function
    # This action is for detail view, use detail view + url_path
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a recipe"""
        # Retrieve the recipe object that is being accessed based on ID in URL
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )
        # validate that the data is all correct
        if serializer.is_valid():
            # We use ModelSerializer so, we can use .save()
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
