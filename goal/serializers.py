from rest_framework import serializers
from .models import *


class salDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = "__all__"

class expDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = "__all__"

class goalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = "__all__"