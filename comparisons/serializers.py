from rest_framework import serializers


class CompareRequestSerializer(serializers.Serializer):
    url1 = serializers.URLField()
    url2 = serializers.URLField()


class MetricSerializer(serializers.Serializer):
    label = serializers.CharField()
    value1 = serializers.FloatField()
    value2 = serializers.FloatField()
    suffix = serializers.CharField(allow_blank=True, default='')


class FreelancerInfoSerializer(serializers.Serializer):
    name = serializers.CharField()
    url = serializers.URLField()


class CompareResponseSerializer(serializers.Serializer):
    freelancer1 = FreelancerInfoSerializer()
    freelancer2 = FreelancerInfoSerializer()
    metrics = MetricSerializer(many=True)
    winner = serializers.CharField()
