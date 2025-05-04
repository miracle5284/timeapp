import inflection
from rest_framework.renderers import JSONRenderer


class CamelCaseJSONRenderer(JSONRenderer):
    """
    Custom JSON renderer for Django REST Framework that converts all
    outgoing response keys from snake_case to camelCase.

    This is useful for frontend clients (like JavaScript apps) that expect
    camelCase keys while keeping backend logic and serializers Pythonic.
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Converts response data keys to camelCase before rendering JSON.

        Args:
            data: The response data (typically a dict or list).
            accepted_media_type: The media type accepted by the client (optional).
            renderer_context: Additional context about the response (optional).

        Returns:
            A JSON string with camelCase keys.
        """
        # Convert all snake_case keys to camelCase recursively
        camelized_data = self.camelize_keys(data)
        # Call the original DRF renderer with the transformed data
        return super().render(camelized_data, accepted_media_type, renderer_context)

    def camelize_keys(self, obj):
        """
        Recursively convert all dict keys from snake_case to camelCase.

        Args:
            obj: A dictionary, list, or primitive value.

        Returns:
            A new object with keys transformed to camelCase.
        """
        if isinstance(obj, dict):
            # Convert each key in the dictionary to camelCase
            return {inflection.camelize(k, False): self.camelize_keys(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            # Recursively apply camelCase conversion to each item in the list
            return [self.camelize_keys(i) for i in obj]
        # Primitive types are returned unchanged
        return obj
