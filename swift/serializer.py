from rest_framework import serializers
from swift.models import Student

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__' 