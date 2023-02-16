from rest_framework import serializers

from . import models


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = '__all__'


class RetrieveReviewSerializer (serializers.Serializer):
    from_date = serializers.DateTimeField(required=False)
    to_date = serializers.DateTimeField(required=False)
