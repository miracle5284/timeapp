import inflection
from rest_framework import generics

from .parsers import CamelCaseJSONParser
from .renderers import CamelCaseJSONRenderer


class BaseView:
    """
    Base view mixin that provides automatic camelCase to snake_case transformation
    for request parsing and response rendering in Django REST Framework.

    - Converts incoming camelCase JSON keys to snake_case for Python serializers.
    - Converts outgoing snake_case response keys to camelCase for JavaScript clients.
    """

    camelize_response = True  # Enable camelCase rendering for responses
    decamelize_request = True  # Enable snake_case conversion for incoming data

    @property
    def decamelize_query_params(self):
        """
        Converts incoming camelCase query parameters to snake_case.

        Returns:
            dict: Query parameters with snake_case keys.
        """
        return {
            inflection.underscore(k): v
            for k, v in self.request.query_params.items()
        }

    def get_renderers(self):
        """
        Overrides DRF's renderer selection to apply CamelCaseJSONRenderer
        if `camelize_response` is True.

        Returns:
            list: List of renderer instances.
        """
        if self.camelize_response:
            return [CamelCaseJSONRenderer()]
        return super().get_renderers()

    def get_parsers(self):
        """
        Overrides DRF's parser selection to apply CamelCaseJSONParser
        if `decamelize_request` is True.

        Returns:
            list: List of parser instances.
        """
        if self.decamelize_request:
            return [CamelCaseJSONParser()]
        return super().get_parsers()


class BaseCreateAPIView(BaseView, generics.CreateAPIView):
    """
    Base API view for creating resources, with camelCase input/output handling.
    """
    pass


class BaseGenericAPIView(BaseView, generics.GenericAPIView):
    """
    Base generic view with camelCase input/output handling.
    """
    pass


class BaseListUpdateAPIView(BaseView, generics.ListAPIView, generics.UpdateAPIView):
    """
    Base API view that supports listing and updating resources,
    with camelCase support for both input and output.
    """
    pass
