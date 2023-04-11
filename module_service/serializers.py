from rest_framework import serializers
from .models import Tag, TagModule, Module

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

class TagModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagModule
        fields = "__all__"

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = "__all__"
