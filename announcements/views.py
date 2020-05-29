from rest_framework import permissions, serializers
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

from lqdoj_backend.paginations import CustomPagination
from .models import Announcement


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow all readonly request
        if request.method in permissions.SAFE_METHODS:
            return True

        # If it's modification request, check permission
        if request.auth is None:  # Check token
            return False

        return request.user.is_staff  # Check staff permission


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'


class AnnouncementsView(viewsets.ModelViewSet):
    queryset = Announcement.objects.all().order_by("-time")
    serializer_class = AnnouncementSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsStaffOrReadOnly,)
    _paginator = CustomPagination(page_size=5, page_size_query_param="limit", page_query_param="p")
