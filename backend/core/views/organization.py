from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework import status
from core.permissions import (
    IsSuperAdminOrReadOnly,
    IsAuthenticated,
    IsAdminUser,
    IsManager,
    IsSuperAdmin,
)

from core.models import Organization

from core.serializers.organization import (
    OrganizationListSerializer,
    OrganizationDetailSerializer,
)


class OrganizationList(ListCreateAPIView):
    queryset = Organization().get_all_actives()
    serializer_class = OrganizationListSerializer

    # permission_classes = [IsSuperAdminOrReadOnly]
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.kind == "SUPER_ADMIN":
            return Organization().get_all_actives()
        return Organization().get_all_actives().filter(id=user.organization_id)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [(IsAuthenticated)()]
        return [
            (IsAdminUser | IsManager | IsSuperAdmin)()
        ]  # Only Admin and Manager can modify customers


class OrganizationDetail(RetrieveUpdateDestroyAPIView):
    queryset = Organization().get_all_actives()
    serializer_class = OrganizationDetailSerializer
    lookup_field = "uid"
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.kind == "SUPER_ADMIN":
            return Organization().get_all_actives()
        return Organization().get_all_actives().filter(id=user.organization_id)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [(IsAdminUser | IsAuthenticated)()]
        return [
            (IsAdminUser | IsManager | IsSuperAdmin)()
        ]  # Only Admin and Manager can modify customers
