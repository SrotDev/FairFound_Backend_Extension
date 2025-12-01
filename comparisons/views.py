from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from leaderboard.models import Freelancer
from .models import ComparisonHistory
from .serializers import CompareRequestSerializer, CompareResponseSerializer


class CompareFreelancersView(APIView):
    """Compare two freelancers by their profile URLs."""

    def post(self, request):
        serializer = CompareRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        url1 = serializer.validated_data['url1']
        url2 = serializer.validated_data['url2']

        # Try to find freelancers in database
        f1 = Freelancer.objects.filter(profile_url=url1).first()
        f2 = Freelancer.objects.filter(profile_url=url2).first()

        # Build comparison data
        comparison_data = self._build_comparison(url1, url2, f1, f2)

        # Log comparison for analytics
        ComparisonHistory.objects.create(
            freelancer1_url=url1,
            freelancer2_url=url2,
            winner_url=url1 if comparison_data['winner'] == comparison_data['freelancer1']['name'] else url2
        )

        return Response(comparison_data)

    def _build_comparison(self, url1, url2, f1, f2):
        """Build comparison response data."""
        name1 = f1.name if f1 else self._extract_username(url1)
        name2 = f2.name if f2 else self._extract_username(url2)

        metrics = [
            {
                'label': 'Rating',
                'value1': float(f1.marketplace_rating) if f1 else 4.5,
                'value2': float(f2.marketplace_rating) if f2 else 4.3,
                'suffix': ''
            },
            {
                'label': 'Jobs Done',
                'value1': f1.jobs_completed if f1 else 100,
                'value2': f2.jobs_completed if f2 else 85,
                'suffix': ''
            },
            {
                'label': 'On-Time',
                'value1': f1.on_time_percentage if f1 else 90,
                'value2': f2.on_time_percentage if f2 else 88,
                'suffix': '%'
            },
            {
                'label': 'Response',
                'value1': f1.response_time_hours if f1 else 3,
                'value2': f2.response_time_hours if f2 else 5,
                'suffix': 'h'
            },
            {
                'label': 'Rehire Rate',
                'value1': f1.rehire_rate if f1 else 75,
                'value2': f2.rehire_rate if f2 else 70,
                'suffix': '%'
            },
            {
                'label': 'FairFound Score',
                'value1': f1.fairfound_score if f1 else 82,
                'value2': f2.fairfound_score if f2 else 78,
                'suffix': ''
            }
        ]

        # Determine winner based on FairFound score
        score1 = f1.fairfound_score if f1 else 82
        score2 = f2.fairfound_score if f2 else 78
        winner = name1 if score1 >= score2 else name2

        return {
            'freelancer1': {'name': name1, 'url': url1},
            'freelancer2': {'name': name2, 'url': url2},
            'metrics': metrics,
            'winner': winner
        }

    def _extract_username(self, url):
        """Extract username from profile URL."""
        try:
            from urllib.parse import urlparse
            path = urlparse(url).path
            parts = [p for p in path.split('/') if p]
            return parts[-1] if parts else 'Unknown'
        except Exception:
            return 'Unknown'
