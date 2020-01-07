from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from factory.faker import Faker


class UserFactory(DjangoModelFactory):
    username = Faker("pystr", min_chars=2, max_chars=30)
    email = Faker("email")

    class Meta:
        model = get_user_model()
