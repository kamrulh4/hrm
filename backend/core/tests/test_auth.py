from django.urls import reverse
from rest_framework import status
from common.base_test import BaseTest
from core.models import User
from core.choices import UserKind


class AuthenticationTests(BaseTest):
    """Test suite for authentication related functionality"""

    def test_user_login_success(self):
        """Test successful user login"""
        response = self.client.post(
            reverse("user-login"),
            {"email": self.admin_user.email, "password": "testpass123"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)
        self.assertIn("user", response.data)

    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post(
            reverse("user-login"),
            {"email": self.admin_user.email, "password": "wrongpassword"},
        )

        # DRF validation errors for serializer come back as 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration(self):
        """Test user registration by admin"""
        self.authenticate_client(self.admin_user)

        user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            "phone": "+15550000001",
            "password": "testpass123",
            "confirm_password": "testpass123",
            "organization": self.test_organization.id,
            "kind": UserKind.OTHER,
        }

        response = self.client.post(reverse("user-registration"), user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify user was created
        self.assertTrue(User.objects.filter(email="testuser@example.com").exists())

    def test_unauthorized_user_registration(self):
        """Test that regular users cannot register new users"""
        self.authenticate_client(self.regular_user)

        user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser2@example.com",
            "password": "testpass123",
            "organization": self.test_organization.id,
            "kind": UserKind.OTHER,
        }

        response = self.client.post(reverse("user-registration"), user_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_change_password(self):
        """Test password change functionality"""
        self.authenticate_client(self.regular_user)

        password_data = {
            "old_password": "testpass123",
            "new_password": "newtestpass123",
            "confirm_new_password": "newtestpass123",
        }

        response = self.client.post(reverse("change-user-password"), password_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify new password works
        response = self.client.post(
            reverse("user-login"),
            {"email": self.regular_user.email, "password": "newtestpass123"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_refresh(self):
        """Test refresh token functionality"""
        # First login to get tokens
        response = self.client.post(
            reverse("user-login"),
            {"email": self.admin_user.email, "password": "testpass123"},
        )

        refresh_token = response.data["refresh_token"]

        # Try to get new access token
        response = self.client.post(
            reverse("user-login-refresh"), {"refresh_token": refresh_token}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("access_token_exp", response.data)

    def test_me_endpoint(self):
        """Test the me endpoint returns correct user data"""
        self.authenticate_client(self.org_admin)

        response = self.client.get(reverse("me-detail"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.org_admin.email)
        self.assertEqual(response.data["first_name"], self.org_admin.first_name)
        self.assertIn("organization", response.data)
