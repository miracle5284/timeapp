import inflection
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from .parsers import CamelCaseJSONParser
from .renderers import CamelCaseJSONRenderer


class BaseView:
    """
    A reusable base view mixin that enforces camelCase ↔ snake_case transformations
    for API requests and responses in Django REST Framework.

    Features:
    - Converts camelCase JSON input from JavaScript clients to snake_case.
    - Converts snake_case DRF output to camelCase before returning JSON.
    - Automatically applies user-based filtering on queryset.
    """

    camelize_response = True      # Enable camelCase rendering in responses
    decamelize_request = True     # Enable snake_case conversion for incoming JSON

    @property
    def decamelize_query_params(self):
        """
        Transform camelCase query parameters into snake_case for backend use.

        Returns:
            dict: Query parameters with keys converted to snake_case.
        """
        return {
            inflection.underscore(k): v
            for k, v in self.request.query_params.items()
        }

    def get_renderers(self):
        """
        Use custom CamelCaseJSONRenderer if camelize_response is enabled.

        Returns:
            list: List of renderer classes.
        """
        if self.camelize_response:
            return [CamelCaseJSONRenderer()]
        return super().get_renderers()

    def get_parsers(self):
        """
        Use custom CamelCaseJSONParser if decamelize_request is enabled.

        Returns:
            list: List of parser classes.
        """
        if self.decamelize_request:
            return [CamelCaseJSONParser()]
        return super().get_parsers()

    def get_queryset(self):
        """
        Default queryset restricted to objects belonging to the authenticated user.

        Returns:
            QuerySet: User-filtered queryset from the serializer's model.
        """
        serializer_cls = self.get_serializer_class()
        model = serializer_cls.Meta.model
        return model.objects.filter(user_id=self.request.user.id)


class BaseCreateAPIView(BaseView, generics.CreateAPIView):
    """
    Base view for creating resources with automatic camelCase parsing/rendering.
    """
    pass


class BaseGenericAPIView(BaseView, generics.GenericAPIView):
    """
    Generic base view for DRF views that need camelCase JSON compatibility.
    """
    pass


class BaseListUpdateAPIView(BaseView, generics.ListAPIView, generics.UpdateAPIView):
    """
    Base view supporting both list and update operations with camelCase I/O.
    """
    pass


class BaseModelViewSet(BaseView, ModelViewSet):
    """
    Base viewset class with camelCase JSON parsing/rendering and user scoping.
    Suitable for full CRUD ViewSet definitions.
    """
    pass
