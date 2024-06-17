from rest_framework import serializers
from .models import Eval 
from .models import CustomUser
from .models import Team
from djoser.serializers import UserCreateSerializer 


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Serializer for the CustomUser model.
    This serializer is used to handle the creation and updating of user instances, including additional fields
    like 'team' and 'info' which are specific to this application's user model.
    """
    team = serializers.CharField(max_length=100, allow_blank=True, required=False)
    """The team field is a character field for the user's team, allowing a maximum length of 100 characters. 
    This field is optional and can be left blank."""

    info = serializers.CharField(max_length=100, allow_blank=True, required=False)
    """The info field is a character field for additional user information, allowing a maximum length of 100 characters. 
    This field is optional and can be left blank."""

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'team', 'is_superuser', 'info']
        """Specifies the model that this serializer works with and the fields to include in the serialization."""
        extra_kwargs = {'password': {'write_only': True}}
        """The password field is write-only to ensure it is not exposed in read operations."""

    def update(self, instance, validated_data):
        """
        Override the update method of the ModelSerializer.
        This method allows updating a user instance without requiring a password change.
        If the 'password' field is included in the validated data and its value is different from 'nothingtochange',
        the user's password is updated. Otherwise, the password remains unchanged.
        """
        instance.username = validated_data.get('username', instance.username)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        if 'password' in validated_data:
            if validated_data['password'] != "nothingtochange":
                instance.set_password(validated_data['password'])
        instance.team = validated_data.get('team', instance.team)
        instance.info = validated_data.get('info', instance.info)
        instance.save()
        return instance



class EvalSerializer(serializers.ModelSerializer):
    """
    Serializer for the Eval model.
    This serializer is used to handle the conversion of Eval model instances to and from various formats such as JSON.
    It includes all fields from the Eval model.
    """
    class Meta:
        model = Eval
        fields = '__all__'
        """Specifies the model that this serializer works with and includes all fields of the Eval model in the serialization."""


class TeamSerializer(serializers.ModelSerializer):
    """
    Serializer for the Team model.
    This serializer is used to handle the conversion of Team model instances to and from various formats such as JSON.
    It includes all fields from the Team model.
    """
    class Meta:
        model = Team
        fields = '__all__'
        """Specifies the model that this serializer works with and includes all fields of the Team model in the serialization."""
