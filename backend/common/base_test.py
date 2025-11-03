from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from core.models import Organization, Subscription
from core.choices import UserKind, SubscriptionStatus
from common.choices import Status
from core.token_authentication import JWTAuthentication

User = get_user_model()


class BaseTest(APITestCase):
    """Base test class with utility methods for testing the HRM system"""

    def setUp(self):
        """Set up test environment"""
        self.client = APIClient()
        self.setup_test_data()

    def setup_test_data(self):
        """Create basic test data"""
        # Create test users with different roles
        self.admin_user = self.create_user(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            password="testpass123",
            is_superuser=True,
            is_staff=True,
            kind=UserKind.SUPER_ADMIN,
        )

        self.org_admin = self.create_user(
            first_name="Org",
            last_name="Admin",
            email="orgadmin@example.com",
            password="testpass123",
            kind=UserKind.ADMIN,
        )

        self.regular_user = self.create_user(
            first_name="Regular",
            last_name="User",
            email="user@example.com",
            password="testpass123",
            kind=UserKind.OTHER,
        )

        # Create test subscription
        self.test_subscription = Subscription.objects.create(
            name="Test Plan",
            description="Test Subscription Plan",
            price="99.99",
            max_user=10,
            duration_in_days=30,
        )

        # Create test organization
        self.test_organization = Organization.objects.create(
            name="Test Organization",
            description="Test Organization Description",
            subscription=self.test_subscription,
            subscription_status=SubscriptionStatus.ACTIVE,
            status=Status.ACTIVE,
            max_user=5,
        )

        # Associate org_admin with organization
        self.org_admin.organization = self.test_organization
        self.org_admin.save()

    def create_user(
        self, first_name, last_name, email, password, phone=None, **extra_fields
    ):
        """Helper method to create users"""
        if phone is None:
            # Generate a unique phone number based on email to avoid conflicts
            email_hash = str(abs(hash(email)))[:10]
            phone = f"+1{email_hash.zfill(10)}"

        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            phone=phone,
            **extra_fields,
        )

    def authenticate_user(self, email, password):
        """Helper method to authenticate a user and get tokens"""
        response = self.client.post(
            reverse("user-login"), {"email": email, "password": password}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data["access_token"]

    def authenticate_client(self, user=None):
        """Set authentication for the test client"""
        if user is None:
            user = self.admin_user
        # Use internal token generation to avoid depending on the login endpoint
        user_data = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone,
            "email": user.email,
            "kind": user.kind,
            "is_superuser": user.is_superuser,
        }
        access_token, refresh_token, access_exp, refresh_exp = (
            JWTAuthentication.generate_tokens(user_data)
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def create_organization_with_subscription(self, name, subscription=None):
        """Helper method to create an organization with subscription"""
        if subscription is None:
            subscription = self.test_subscription

        return Organization.objects.create(
            name=name,
            description=f"{name} Description",
            subscription=subscription,
            subscription_status=SubscriptionStatus.ACTIVE,
            status=Status.ACTIVE,
            max_user=5,
        )

    def create_user_with_org(
        self, first_name, last_name, email, organization, kind=UserKind.OTHER
    ):
        """Helper method to create a user associated with an organization"""
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password="testpass123",
            kind=kind,
        )
        user.organization = organization
        user.save()
        return user
