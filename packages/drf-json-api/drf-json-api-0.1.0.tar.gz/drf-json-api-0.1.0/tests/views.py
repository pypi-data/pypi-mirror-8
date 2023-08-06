from django.http import HttpResponse
from rest_framework import viewsets
from tests import models
from tests import serializers


class EchoMixin(object):
    """
    Returns the parsed data that was sent in the request when a ECHO request
    is made to the view.
    """

    http_method_names = viewsets.ModelViewSet.http_method_names + ["echo"]

    def echo(self, request, *args, **kwargs):
        response = HttpResponse("echo")
        response.data = request.DATA

        return response


class CommentViewSet(EchoMixin, viewsets.ModelViewSet):
    model = models.Comment
    serializer_class = serializers.CommentSerializer


class PersonViewSet(EchoMixin, viewsets.ModelViewSet):
    model = models.Person
    serializer_class = serializers.PersonSerializer


class PostViewSet(EchoMixin, viewsets.ModelViewSet):
    model = models.Post
    serializer_class = serializers.PostSerializer


class MaximalPersonViewSet(viewsets.ModelViewSet):
    model = models.Person
    serializer_class = serializers.MaximalPersonSerializer


class NestedCommentViewSet(CommentViewSet):
    serializer_class = serializers.NestedCommentSerializer


class NestedPostViewSet(PostViewSet):
    serializer_class = serializers.NestedPostSerializer


class PkCommentViewSet(CommentViewSet):
    serializer_class = serializers.PkCommentSerializer


class PkMaximalPersonViewSet(viewsets.ModelViewSet):
    model = models.Person
    serializer_class = serializers.PkMaximalPersonSerializer
