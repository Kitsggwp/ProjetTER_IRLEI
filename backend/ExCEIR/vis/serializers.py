from rest_framework import serializers
from .models import Eval 

class EvalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eval
        fields = '__all__'