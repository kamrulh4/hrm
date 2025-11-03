from django.urls import reverse
from rest_framework import status
from common.base_test import BaseTest
from core.models import Organization
from core.choices import SubscriptionStatus
from common.choices import Status


class OrganizationTests(BaseTest):
    """Test suite for organization management"""

    def test_create_organization(self):
        """Test creating a new organization"""
        self.authenticate_client(self.admin_user)

        org_data = {
            "name": "New Test Organization",
            "description": "Test Description",
            "address": "Test Address",
            "phone": "+1234567890",
            "country": "Test Country",
            "email": "org@example.com",
            "website": "https://example.com",
            "subscription": self.test_subscription.id,
            "max_user": 10,
        }

        response = self.client.post(reverse("organization-list"), org_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], org_data["name"])

        # Verify organization was created
        self.assertTrue(
            Organization.objects.filter(name="New Test Organization").exists()
        )

    def test_list_organizations(self):
        """Test listing organizations"""
        self.authenticate_client(self.admin_user)

        # Create additional test organizations
        self.create_organization_with_subscription("Org 1")
        self.create_organization_with_subscription("Org 2")

        response = self.client.get(reverse("organization-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Including the test organization created in setUp
        self.assertTrue(len(response.data) >= 3)

    def test_update_organization(self):
        """Test updating an organization"""
        self.authenticate_client(self.admin_user)

        update_data = {
            "name": "Updated Organization Name",
            "description": "Updated Description",
            "max_user": 15,
        }

        response = self.client.patch(
            reverse("organization-detail", kwargs={"uid": self.test_organization.uid}),
            update_data,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], update_data["name"])
        self.assertEqual(response.data["max_user"], update_data["max_user"])

    def test_delete_organization(self):
        """Test deleting an organization"""
        self.authenticate_client(self.admin_user)

        response = self.client.delete(
            reverse("organization-detail", kwargs={"uid": self.test_organization.uid})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Verify organization has been deleted (endpoint performs hard delete)
        self.assertFalse(
            Organization.objects.filter(uid=self.test_organization.uid).exists()
        )

    def test_organization_subscription_status(self):
        """Test organization subscription status update"""
        self.authenticate_client(self.admin_user)

        update_data = {
            "subscription_status": SubscriptionStatus.ACTIVE,
            "subscription": self.test_subscription.id,
        }

        response = self.client.patch(
            reverse("organization-detail", kwargs={"uid": self.test_organization.uid}),
            update_data,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["subscription_status"], SubscriptionStatus.ACTIVE
        )

    def test_org_admin_access_restrictions(self):
        """Test that org admins can only access their own organization"""
        self.authenticate_client(self.org_admin)

        # Create another organization
        other_org = self.create_organization_with_subscription("Other Org")

        # Try to access other organization
        response = self.client.get(
            reverse("organization-detail", kwargs={"uid": other_org.uid})
        )
        # The view filters queryset by the user's organization, so accessing another org
        # returns 404 (not found) rather than 403.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_regular_user_organization_access(self):
        """Test that regular users cannot modify organizations"""
        self.authenticate_client(self.regular_user)

        update_data = {"name": "Unauthorized Update"}

        response = self.client.patch(
            reverse("organization-detail", kwargs={"uid": self.test_organization.uid}),
            update_data,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
