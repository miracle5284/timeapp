import uuid

import factory
from django.contrib.auth import get_user_model

User = get_user_model()
USER_TEST_PASSWORD = 'testPass@123'

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True  # ✅ avoids implicit save warning

    email = factory.LazyFunction(lambda: f"{uuid.uuid4().hex}@example.com")
    password = USER_TEST_PASSWORD

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # Set raw password and encrypt it properly
        raw_password = kwargs.pop("password", USER_TEST_PASSWORD)
        user = model_class(*args, **kwargs)
        user.set_password(raw_password)
        user.save()
        return user