import inflection
from rest_framework.parsers import JSONParser


class CamelCaseJSONParser(JSONParser):
    """
    Custom JSON parser for Django REST Framework that converts incoming
    camelCase JSON keys into snake_case before passing data to serializers.

    This ensures that frontend clients using camelCase can seamlessly interact
    with DRF backends expecting Pythonic snake_case field names.
    """

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Parses the incoming bytestream and converts camelCase keys to snake_case.

        Args:
            stream: The raw bytestream from the request body.
            media_type: The media type of the incoming content (optional).
            parser_context: Additional context about the request (optional).

        Returns:
            A Python object (usually a dict or list) with all keys in snake_case.
        """
        # First, parse the raw JSON body using the standard DRF JSON parser
        data = super().parse(stream, media_type=media_type, parser_context=parser_context)
        # Then recursively convert all camelCase keys to snake_case
        return self.decamelize_keys(data)

    def decamelize_keys(self, obj):
        """
        Recursively converts all camelCase dictionary keys to snake_case.

        Args:
            obj: A dictionary, list, or primitive type.

        Returns:
            A new object with all keys converted to snake_case if applicable.
        """
        if isinstance(obj, dict):
            # Apply conversion to each key-value pair recursively
            return {inflection.underscore(k): self.decamelize_keys(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            # Apply conversion to each item in the list recursively
            return [self.decamelize_keys(item) for item in obj]
        # Base case: return primitive types as-is
        return obj
