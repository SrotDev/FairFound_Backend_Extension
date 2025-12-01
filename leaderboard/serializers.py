from rest_framework import serializers
from .models import Freelancer


class FreelancerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Freelancer
        fields = [
            'id', 'name', 'profile_url', 'specialty', 'platform',
            'marketplace_rating', 'marketplace_score', 'fairfound_score',
            'jobs_completed', 'on_time_percentage', 'response_time_hours',
            'rehire_rate'
        ]


class LeaderboardSerializer(serializers.ModelSerializer):
    """Simplified serializer for leaderboard display."""
    score = serializers.SerializerMethodField()

    class Meta:
        model = Freelancer
        fields = ['id', 'name', 'specialty', 'score']

    def get_score(self, obj):
        ranking_type = self.context.get('ranking_type', 'fairfound')
        if ranking_type == 'marketplace':
            return obj.marketplace_score
        return obj.fairfound_score
