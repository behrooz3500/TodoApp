# dj
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

# rest
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

# account api
from ..serializers import ProfileSerializer
from accounts.models import Profile

User = get_user_model()


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    model = Profile
    queryset = model.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.queryset, user__email=self.request.user)
        return obj
