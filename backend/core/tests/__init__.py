import factory
from factory.django import DjangoModelFactory
from faker import Faker
from datetime import date, timedelta
import random

from core.models import (
    Subscription,
    Organization,
    User,
    OTP,
)
from core.choices import (
    SubscriptionStatus,
    UserKind,
    UserGender,
    OTPType,
)
from common.choices import Status

fake = Faker()


class SubscriptionFactory(DjangoModelFactory):
    """Factory for Subscription model."""

    class Meta:
        model = Subscription

    name = factory.LazyAttribute(lambda _: fake.word().capitalize() + " Plan")
    description = factory.LazyAttribute(lambda _: fake.sentence(nb_words=8))
    price = factory.LazyAttribute(lambda _: round(random.uniform(10, 200), 2))
    max_user = factory.LazyAttribute(lambda _: random.randint(5, 50))
    duration_in_days = factory.LazyAttribute(lambda _: random.choice([30, 60, 90, 365]))


class OrganizationFactory(DjangoModelFactory):
    """Factory for Organization model."""

    class Meta:
        model = Organization

    name = factory.LazyAttribute(lambda _: fake.company())
    description = factory.LazyAttribute(lambda _: fake.catch_phrase())
    address = factory.LazyAttribute(lambda _: fake.address())
    phone = factory.LazyAttribute(lambda _: fake.phone_number())
    country = factory.LazyAttribute(lambda _: fake.country())
    owner = factory.LazyAttribute(lambda _: fake.name())
    email = factory.LazyAttribute(lambda _: fake.company_email())
    website = factory.LazyAttribute(lambda _: fake.url())
    metadata = factory.LazyAttribute(lambda _: {"industry": fake.word()})
    logo = factory.LazyAttribute(lambda _: fake.image_url())
    subscription = factory.Iterator(Subscription().get_all_actives())
    subscription_start = factory.LazyFunction(date.today)
    subscription_end = factory.LazyAttribute(
        lambda o: o.subscription_start
        + timedelta(days=random.choice([30, 60, 90, 365]))
    )
    total_leave = factory.LazyAttribute(lambda _: random.randint(5, 30))
    max_user = factory.LazyAttribute(lambda _: random.randint(5, 50))
    total_user = factory.LazyAttribute(lambda _: random.randint(1, 20))
    subscription_status = factory.LazyAttribute(
        lambda _: random.choice(SubscriptionStatus.values)
    )
    status = factory.LazyAttribute(lambda _: random.choice(Status.values))


class UserFactory(DjangoModelFactory):
    """Factory for User model."""

    class Meta:
        model = User

    organization = factory.Iterator(Organization().get_all_actives())
    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
    email = factory.LazyAttribute(
        lambda o: f"{o.first_name.lower()}.{o.last_name.lower()}@{fake.free_email_domain()}"
    )
    phone = factory.LazyAttribute(lambda _: fake.msisdn()[:11])
    gender = factory.LazyAttribute(lambda _: random.choice(UserGender.values))
    is_active = True
    is_staff = factory.LazyAttribute(lambda _: fake.boolean(chance_of_getting_true=20))
    is_superuser = factory.LazyAttribute(
        lambda _: fake.boolean(chance_of_getting_true=10)
    )
    is_verified = factory.LazyAttribute(
        lambda _: fake.boolean(chance_of_getting_true=60)
    )
    kind = factory.LazyAttribute(lambda _: random.choice(UserKind.values))
    password = factory.PostGenerationMethodCall("set_password", "12345678")


class OTPFactory(DjangoModelFactory):
    """Factory for OTP model."""

    class Meta:
        model = OTP

    user = factory.Iterator(User().get_all_actives())
    code = factory.LazyAttribute(lambda _: str(random.randint(100000, 999999)))
    is_used = factory.LazyAttribute(lambda _: fake.boolean(chance_of_getting_true=30))
    otp_type = factory.LazyAttribute(lambda _: random.choice(OTPType.values))
