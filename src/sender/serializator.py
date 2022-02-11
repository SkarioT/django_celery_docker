import code
from venv import create
from django.forms import SlugField, fields
from rest_framework import serializers
from .models import Client,Send_out


class ClienSerializator(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
