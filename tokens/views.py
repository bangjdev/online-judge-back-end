import json

from django.contrib.auth import authenticate
from rest_framework import mixins, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.viewsets import GenericViewSet


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'


class TokenView(mixins.CreateModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet):
    serializer_class = TokenSerializer
    queryset = Token.objects.all()
    authentication_classes = [TokenAuthentication]
    lookup_field = "key"

    """
    Login handler: POST request to /tokens/ to create a new token
    Return 200 if success, 401 if the credentials aren't good, 500 if server error
    """

    def create(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                token, created = self.queryset.get_or_create(user=user)
                return Response(data={'token': token.key}, status=HTTP_200_OK)
            else:
                return Response(status=HTTP_401_UNAUTHORIZED)
        except:
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

    """
    Logout handler: DELETE request to /tokens/ to delete token
    Return 200 if success, or 401 if token was not supplied
    """

    def destroy(self, request, *args, **kwargs):
        try:
            token = request.auth
            if token.key != kwargs['key']:
                return Response(status=HTTP_401_UNAUTHORIZED)
            self.queryset.get(key=token).delete()
            return Response(status=HTTP_200_OK)
        except:
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)
