from rest_framework import parsers, renderers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from vending.apps.vauth.models import MultiToken
from vending.apps.vauth.serializers import MultiTokenSerializer


class ObtainAuthToken(APIView):
    """
    Giver Username Password provides API Token for Auth
    """

    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = MultiToken.objects.create(user=user)
        total = MultiToken.objects.filter(user=user).count()
        resp = {'token': token.key, 'total_tokens': total}
        if total > 1:
            resp['msg'] = "There is already an active session using your account"
        return Response(resp)


class KillAuthToken(APIView):
    """
    Receives token as argument and ends session/delete token
    """
    throttle_classes = ()
    permission_classes = (IsAuthenticated, )
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = MultiTokenSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        MultiToken.objects.filter(user=request.user, key=token).delete()
        return Response({'msg': 'Token deleted if valid token provided.'})


class KillAllAuthTokens(APIView):
    throttle_classes = ()
    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, *args, **kwargs):
        MultiToken.objects.filter(user=request.user).delete()
        return Response({'msg': 'All tokens deleted.'})
