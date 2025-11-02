"""Core models for our app."""

from django.contrib.auth.base_user import (
    BaseUserManager,
)
from django.contrib.auth.models import AbstractBaseUser
from django.db import models


from common.models import BaseModelWithUID, NameDescriptionBaseModel
from common.choices import Status
from core.choices import (
    UserKind,
    UserGender,
    SubscriptionType,
    SubscriptionStatus,
    OTPType,
    BillingCycle,
)
from core.utils import get_user_media_path_prefix


class Subscription(NameDescriptionBaseModel):
    """Subscription model."""

    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_user = models.PositiveIntegerField(default=5)
    duration_in_days = models.PositiveIntegerField(default=30)

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        # ordering = ["-pk"]

    def __str__(self):
        return self.name


class Organization(NameDescriptionBaseModel):
    """Model representing an organization."""

    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=128, blank=True, null=True)
    owner = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True, default=dict)
    logo = models.URLField(blank=True, null=True)
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="companies",
    )
    subscription_start = models.DateField(blank=True, null=True)
    subscription_end = models.DateField(blank=True, null=True)
    total_leave = models.IntegerField(default=0)
    max_user = models.IntegerField(default=5)
    total_user = models.IntegerField(default=0)
    subscription_status = models.CharField(
        max_length=50,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.PENDING,
    )
    status = models.CharField(
        max_length=50,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"
        ordering = ["-pk"]


class UserManager(BaseUserManager):
    """Managers for users."""

    def create_user(self, first_name, last_name, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email address.")

        user = self.model(
            first_name=first_name, last_name=last_name, email=email, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, first_name, last_name, email, password):
        """Create a new superuser and return superuser"""

        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )

        user.is_superuser = True
        user.is_staff = True
        user.kind = UserKind.SUPER_ADMIN
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, BaseModelWithUID):
    """Users in the System"""

    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        related_name="users",
        null=True,
        blank=True,
        help_text="The organization this user belongs to.",
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        db_index=True,
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        db_index=True,
    )
    phone = models.CharField(
        max_length=20,
        db_index=True,
        unique=True,
        blank=True,
        verbose_name="Phone Number",
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        db_index=True,
    )
    gender = models.CharField(
        max_length=20,
        blank=True,
        choices=UserGender.choices,
        default=UserGender.UNKNOWN,
    )
    is_active = models.BooleanField(
        default=True,
    )
    is_staff = models.BooleanField(
        default=False,
    )
    is_superuser = models.BooleanField(
        default=False,
    )
    is_verified = models.BooleanField(
        default=False,
    )
    kind = models.CharField(
        max_length=20,
        choices=UserKind.choices,
        default=UserKind.OTHER,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = (
        "first_name",
        "last_name",
    )

    def has_perm(self, perm, obj=None):
        return self.is_staff or self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_staff or self.is_superuser

    class Meta:
        verbose_name = "System User"
        verbose_name_plural = "System Users"


class OTP(BaseModelWithUID):
    """Model to store OTPs for user verification."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="otps",
    )
    code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    otp_type = models.CharField(
        max_length=30,
        choices=OTPType.choices,
        default=OTPType.PASSWORD_RESET,
    )

    def __str__(self):
        return f"OTP for {self.user.phone} - {'Used' if self.is_used else 'Unused'}"

    class Meta:
        verbose_name = "OTP"
        verbose_name_plural = "OTPs"
        ordering = ("-pk",)
