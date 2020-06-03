from rest_framework import permissions, serializers
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.status import *

from django.template.defaultfilters import truncatechars_html

from lqdoj_backend.paginations import CustomPagination
from .models import Announcement
from lqdoj_backend.json_response import *


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.method)
        # Allow all readonly request
        if request.method in permissions.SAFE_METHODS:
            return True

        # If it's modification request, check permission
        if request.auth is None:  # Check token
            return False

        return request.user.is_staff  # Check staff permission


class AnnouncementDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'


class AnnouncementSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = '__all__'

    def get_content(self, announcement):
        return truncatechars_html(announcement.content, 200)


class AnnouncementsView(viewsets.ModelViewSet):
    queryset = Announcement.objects.all().order_by("-time")
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsStaffOrReadOnly,)
    _paginator = CustomPagination(
        page_size=5, page_size_query_param="limit", page_query_param="p")
    
    """
    Override retrieve function to customize the response's format
    """
    def retrieve(self, request, *args, **kwargs):
        announcement = self.get_queryset().get(id=kwargs['pk'])
        serialized_announcement = AnnouncementDetailSerializer(announcement).data
        return Response(data=create_message(
                                    message_code="LOADED_SUCCESSFULLY",
                                    results=serialized_announcement),
                        status=HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AnnouncementDetailSerializer
        else:
            return AnnouncementSerializer
