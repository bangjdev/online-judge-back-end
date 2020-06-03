import json

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.http.multipartparser import MultiPartParser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED,
                                   HTTP_403_FORBIDDEN)
from rest_framework.viewsets import ModelViewSet

from users.forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from users.serializers import UserSerializer

from lqdoj_backend.json_response import *


class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"

    """
    Retrieve the current user associated with the token. Returns 200 on
    success, 401 if the token is missing.
    """

    @action(detail=False)
    def me(self, request):
        if request.auth is None:  # Check token
            return Response(status=HTTP_401_UNAUTHORIZED)
        user = request.user  # Retrieve user from token
        serialized = UserSerializer(user)
        return Response(data=create_message(results=serialized.data), status=HTTP_200_OK)

    """
    Custom create function to create users, using custom UserRegistrationForm
    """

    def create(self, request, *args, **kwargs):
        form=UserRegistrationForm(data=json.loads(request.body))
        if form.is_valid():  # Check form data
            form.save()
            return Response(status=HTTP_201_CREATED)
        else:
            return Response(data=form.errors, status=HTTP_400_BAD_REQUEST)

    """
    Custom function to handle PATCH request, use to change user password
    """

    def partial_update(self, request, *args, **kwargs):
        # Return 401 if no token found
        if request.auth is None:
            return Response(status=HTTP_401_UNAUTHORIZED)

        # Return 403 if token doesn't match with the lookup value
        if request.user.username != kwargs[self.lookup_field]:
            return Response(status=HTTP_403_FORBIDDEN)

        form=PasswordChangeForm(data=json.loads(
            request.body), user=request.user)
        if form.is_valid():
            form.save()
            return Response(status=HTTP_200_OK)
        else:
            return Response(data=form.errors, status=HTTP_400_BAD_REQUEST)

    """
    Custom function to handle PUT request, use to change user infos
    """

    def update(self, request, *args, **kwargs):
        # Return 401 if no token found
        if request.auth is None:
            return Response(status=HTTP_401_UNAUTHORIZED)

        # Return 403 if token doesn't match with the lookup value
        if request.user.username != kwargs[self.lookup_field]:
            return Response(status=HTTP_403_FORBIDDEN)

        u_form=UserUpdateForm(data=request.data, instance=request.user)
        p_form=ProfileUpdateForm(data=request.data.dict(
        ), files=request.FILES, instance=request.user.profile)

        if u_form.is_valid():
            u_form.save()
            p_form.save()
            return Response(status=HTTP_200_OK)
        else:
            return_data=u_form.errors
            if u_form.is_valid():
                return_data=p_form.errors
            return Response(data=return_data, status=HTTP_400_BAD_REQUEST)
