from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('pub_date', 'author')

    def create(self, validated_data):
        return Post.objects.create(**validated_data)
