from utils.renderers import CamelCaseJSONRenderer

def test_snake_to_camel_case_render():
    renderer = CamelCaseJSONRenderer()
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "user_details": {
            "postal_code": "12345"
        }
    }

    rendered = renderer.render(data)
    assert b"firstName" in rendered
    assert b"postalCode" in rendered
