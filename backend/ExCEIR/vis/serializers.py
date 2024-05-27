from rest_framework import serializers
from .models import Eval 
from .models import CustomUser
from .models import Team
from djoser.serializers import UserCreateSerializer 


class CustomUserCreateSerializer(UserCreateSerializer):
    team = serializers.CharField(max_length=100)
    info = serializers.CharField(max_length=100)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'team', 'is_superuser', 'info']
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.team = validated_data.get('team', instance.team)
        instance.save()
        return instance


class EvalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eval
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
