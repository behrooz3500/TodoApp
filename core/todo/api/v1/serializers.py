# rest
from rest_framework import serializers

# internal
from todo.models import Todo, TaskCategory
from accounts.models import Profile


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for TaskCategory model"""

    absolute_api_url = serializers.SerializerMethodField(method_name="get_absolute_url")

    class Meta:
        model = TaskCategory
        fields = [
            "id",
            "name",
            "absolute_api_url",
        ]

    def get_absolute_url(self, obj):
        """Retrieving absolute url for a given Category."""

        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        """Managing the representation of Categories in different views."""

        request = self.context.get("request")
        displayed_data = super().to_representation(instance)
        if request.parser_context.get("kwargs").get("pk"):
            displayed_data.pop("absolute_api_url", None)

        return displayed_data


class TodoSerializer(serializers.ModelSerializer):
    """Serializer for Todo model (tasks)"""

    has_been_updated = serializers.BooleanField(read_only=True)
    relative_api_url = serializers.URLField(
        source="get_relative_api_url", read_only=True
    )
    absolute_api_url = serializers.SerializerMethodField(method_name="get_absolute_url")

    # Different ways to customize a fields shown value
    # category = serializers.SlugRelatedField(many=False, slug_field='name', queryset=TaskCategory.objects.all())
    # category = CategorySerializer()

    class Meta:
        model = Todo
        fields = (
            "id",
            "user",
            "title",
            "category",
            "relative_api_url",
            "absolute_api_url",
            "completed",
            "has_been_updated",
            "created_date",
            "updated_date",
        )
        read_only_fields = ["user"]

    def get_absolute_url(self, obj):
        """Retrieving absolute url for a given task."""

        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        """Managing the representation of tasks in different views."""

        request = self.context.get("request")
        displayed_data = super().to_representation(instance)
        # displayed_data["category"] = CategorySerializer(instance.category).data
        if request.parser_context.get("kwargs").get("pk"):
            displayed_data.pop("relative_api_url", None)
            displayed_data.pop("absolute_api_url", None)

        return displayed_data

    def create(self, validated_data):
        """
         Overriding create class to include aythenticated user info in
        task creation form.
        """

        validated_data["user"] = Profile.objects.filter(
            user__id=self.context.get("request").user.id
        )[0]
        return super().create(validated_data)
