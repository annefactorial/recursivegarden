from rest_framework import serializers 


class CardSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.CharField(max_length=1023)
    data = serializers.JSONField()


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
