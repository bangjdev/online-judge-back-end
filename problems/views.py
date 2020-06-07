from django.shortcuts import render

from rest_framework import permissions, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.status import *

from lqdoj_backend.json_response import *
from problems.models import Problem
from problems.serializers import ProblemListSerializer, ProblemSerializer


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow all readonly request
        if request.method in permissions.SAFE_METHODS:
            return True

        # If it's modification request, check permission
        if request.auth is None:  # Check token
            return False

        return request.user.is_staff  # Check staff permission


class ProblemsView(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Problem.objects.all()
    # permission_classes = (IsStaffOrReadOnly,)
    # authentication_classes = [TokenAuthentication]

    """
    Override list function to customize the response's format
    """
    def list(self, request, *args, **kwargs):
        problems_list = self.get_queryset()
        serialized_problems_list = ProblemListSerializer(problems_list, many=True).data        
        return Response(data=create_message(
                                        message_code="LOADED_SUCCESSFULLY", 
                                        results=serialized_problems_list), 
                        status=HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):        
        problem = self.get_queryset().get(problem_code=kwargs['pk'])
        serialized_problem = ProblemSerializer(problem).data
        return Response(data=create_message(
                                        message_code="LOADED_SUCCESSFULLY", 
                                        results=serialized_problem), 
                        status=HTTP_200_OK)


