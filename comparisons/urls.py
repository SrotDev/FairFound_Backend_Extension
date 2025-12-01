from django.urls import path
from .views import CompareFreelancersView

urlpatterns = [
    path('', CompareFreelancersView.as_view(), name='compare-freelancers'),
]
