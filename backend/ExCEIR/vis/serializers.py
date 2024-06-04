from rest_framework import serializers
from .models import Eval 
from .models import CustomUser
from .models import Team
from djoser.serializers import UserCreateSerializer 


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Serializer for the user table
    """
    team = serializers.CharField(max_length=100, allow_blank=True, required=False)
    info = serializers.CharField(max_length=100, allow_blank=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'team', 'is_superuser', 'info']
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        """
        Method which overrides that of the ModelSerializer to be able to update a user without necessarily changing the password
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
    Serializer for the eval table
     """
    class Meta:
        model = Eval
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    """
    Serializer for the team table
    """
    class Meta:
        model = Team
        fields = '__all__'
