from rest_framework import serializers
from .models import Eval 
from .models import CustomUser
from .models import Team
from djoser.serializers import UserCreateSerializer 

class CustomUserCreateSerializer(UserCreateSerializer):
    team = serializers.CharField(max_length=100)

    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'team')

class EvalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eval
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'