# dj

from django.contrib.auth import get_user_model

# rest
from rest_framework import serializers


# internal
from accounts.models import Profile

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    """ User profile serializer """
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'user',
            'email',
            'username',
            'first_name',
            'last_name',
            'image',
            'birth_date',
        ]
        read_only_fields = ['user', 'email']