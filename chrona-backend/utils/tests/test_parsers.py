import io
import json
from utils.parsers import CamelCaseJSONParser
from rest_framework.test import APIRequestFactory

def test_camel_case_parser_conversion():
    parser = CamelCaseJSONParser()

    data = {
        "firstName": "John",
        "lastName": "Doe",
        "address": {"postalCode": "12345"}
    }

    stream = io.BytesIO(json.dumps(data).encode("utf-8"))
    parsed = parser.parse(stream, media_type="application/json", parser_context={})

    assert parsed["first_name"] == "John"
    assert parsed["address"]["postal_code"] == "12345"
