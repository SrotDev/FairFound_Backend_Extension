from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Freelancer
from .serializers import FreelancerSerializer, LeaderboardSerializer


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for leaderboard endpoints."""
    queryset = Freelancer.objects.all()
    serializer_class = FreelancerSerializer

    def _filter_by_category(self, queryset, request):
        """Filter queryset by specialty category if provided."""
        category = request.query_params.get('category', '').strip()
        if category and category.lower() != 'all':
            queryset = queryset.filter(specialty__iexact=category)
        return queryset

    @action(detail=False, methods=['get'])
    def marketplace(self, request):
        """Get marketplace ranking leaderboard with optional category filter."""
        queryset = self._filter_by_category(
            Freelancer.objects.order_by('-marketplace_score'), request
        )[:20]
        serializer = LeaderboardSerializer(
            queryset, many=True, context={'ranking_type': 'marketplace'}
        )
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def fairfound(self, request):
        """Get FairFound ranking leaderboard with optional category filter."""
        queryset = self._filter_by_category(
            Freelancer.objects.order_by('-fairfound_score'), request
        )[:20]
        serializer = LeaderboardSerializer(
            queryset, many=True, context={'ranking_type': 'fairfound'}
        )
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get list of available freelancer categories."""
        categories = Freelancer.objects.values_list('specialty', flat=True).distinct().order_by('specialty')
        return Response(list(categories))

    @action(detail=False, methods=['get'])
    def profiles(self, request):
        """Get list of all freelancers with their profile URLs for comparison."""
        search = request.query_params.get('search', '').strip()
        queryset = Freelancer.objects.all().order_by('name')
        if search:
            queryset = queryset.filter(name__icontains=search)
        freelancers = queryset[:50].values('id', 'name', 'specialty', 'profile_url', 'fairfound_score')
        return Response(list(freelancers))
