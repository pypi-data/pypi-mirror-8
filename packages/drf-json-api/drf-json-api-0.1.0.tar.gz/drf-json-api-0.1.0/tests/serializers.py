from rest_framework import relations, serializers
from tests import models


class CommentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        fields = ("id", "url", "post", "body", )
        model = models.Comment


class PersonSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        fields = ("id", "url", "name", )
        model = models.Person


class PostSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        fields = ("id", "url", "title", "author", "comments", )
        model = models.Post


class MaximalPersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = ("id", "url", "name", "favorite_post", "liked_comments")
        model = models.Person


class MinimalCommentSerializer(CommentSerializer):

    class Meta(CommentSerializer.Meta):
        fields = ("id", "url", "body", )


class MinimalPostSerializer(PostSerializer):

    class Meta(PostSerializer.Meta):
        fields = ("id", "url", "title", )


class NestedCommentSerializer(CommentSerializer):
    post = MinimalPostSerializer()


class NestedPostSerializer(PostSerializer):
    comments = MinimalCommentSerializer(many=True)


class PkCommentSerializer(CommentSerializer):
    post = relations.PrimaryKeyRelatedField()


class PkMaximalPersonSerializer(MaximalPersonSerializer):
    favorite_post = relations.PrimaryKeyRelatedField(null=True)
    liked_comments = relations.PrimaryKeyRelatedField(many=True)
