from rest_framework import serializers

    # Serializer za ustvarjanje novega prihoda
class ArrivalCreateSerializer(serializers.Serializer):
    card_number = serializers.CharField()      # Številka kartice
    arrived_at = serializers.DateTimeField()   # Datum in čas prihoda

# Serializer za prihod z uporabo kartice v trenutku
class ArrivalByCardNowSerializer(serializers.Serializer):
    card_number = serializers.CharField()      # Številka kartice