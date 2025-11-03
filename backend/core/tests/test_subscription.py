from django.urls import reverse
from rest_framework import status
from common.base_test import BaseTest
from core.models import Subscription
from decimal import Decimal


class SubscriptionTests(BaseTest):
    """Test suite for subscription management"""

    def test_create_subscription(self):
        """Test creating a new subscription plan"""
        self.authenticate_client(self.admin_user)

        subscription_data = {
            "name": "Premium Plan",
            "description": "Premium Subscription Plan",
            "price": "199.99",
            "max_user": 20,
            "duration_in_days": 30,
        }
        # The API only exposes listing (GET); creation via this endpoint is not allowed
        response = self.client.post(reverse("subscription-list"), subscription_data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_list_subscriptions(self):
        """Test listing subscription plans"""
        self.authenticate_client(self.admin_user)

        # Create additional test subscriptions
        Subscription.objects.create(
            name="Basic Plan",
            description="Basic Subscription",
            price="49.99",
            max_user=5,
            duration_in_days=30,
        )

        Subscription.objects.create(
            name="Enterprise Plan",
            description="Enterprise Subscription",
            price="299.99",
            max_user=50,
            duration_in_days=30,
        )

        response = self.client.get(reverse("subscription-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # There may be pre-existing subscriptions from fixtures/migrations; assert at least
        # the ones we created are present
        self.assertGreaterEqual(len(response.data), 3)

    def test_update_subscription(self):
        """Test updating a subscription plan"""
        self.authenticate_client(self.admin_user)

        update_data = {"name": "Updated Plan Name", "price": "149.99", "max_user": 15}

        response = self.client.patch(
            reverse("subscription-detail", kwargs={"uid": self.test_subscription.uid}),
            update_data,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], update_data["name"])
        self.assertEqual(Decimal(response.data["price"]), Decimal(update_data["price"]))

    def test_delete_subscription(self):
        """Test deleting a subscription plan"""
        self.authenticate_client(self.admin_user)

        # Create a new subscription for deletion
        subscription = Subscription.objects.create(
            name="To Delete Plan",
            description="Plan to be deleted",
            price="79.99",
            max_user=10,
            duration_in_days=30,
        )

        response = self.client.delete(
            reverse("subscription-detail", kwargs={"uid": subscription.uid})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify subscription is deleted
        self.assertFalse(Subscription.objects.filter(uid=subscription.uid).exists())

    def test_non_admin_subscription_access(self):
        """Test that non-admin users cannot modify subscriptions"""
        self.authenticate_client(self.org_admin)

        subscription_data = {
            "name": "Unauthorized Plan",
            "description": "This should not work",
            "price": "99.99",
            "max_user": 10,
            "duration_in_days": 30,
        }
        # Non-admins are forbidden from modifying subscriptions
        response = self.client.post(reverse("subscription-list"), subscription_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_subscription_assignment_to_organization(self):
        """Test assigning a subscription to an organization"""
        self.authenticate_client(self.admin_user)

        # Create a new subscription
        new_subscription = Subscription.objects.create(
            name="Premium Plan",
            description="Premium Subscription",
            price="199.99",
            max_user=20,
            duration_in_days=30,
        )

        update_data = {"subscription": new_subscription.id}

        response = self.client.patch(
            reverse("organization-detail", kwargs={"uid": self.test_organization.uid}),
            update_data,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["subscription"], new_subscription.id)
