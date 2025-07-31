import factory
from ..models import Timers
from django.utils import timezone


TEST_DURATION = 300


class TimerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Timers

    # user_id = factory.SubFactory('users.tests.factories.UserFactory')
    name = factory.Faker('word')
    duration_seconds = TEST_DURATION
    status = 'pending'
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)