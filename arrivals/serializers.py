from rest_framework import serializers

class ArrivalCreateSerializer(serializers.Serializer):
    card_number = serializers.CharField()
    arrived_at = serializers.DateTimeField()

class ArrivalByCardNowSerializer(serializers.Serializer):
    card_number = serializers.CharField()