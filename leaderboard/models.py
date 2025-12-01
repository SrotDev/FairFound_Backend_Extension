from django.db import models


class Freelancer(models.Model):
    """Freelancer profile with marketplace and FairFound scores."""
    
    name = models.CharField(max_length=200)
    profile_url = models.URLField(unique=True)
    specialty = models.CharField(max_length=100)
    platform = models.CharField(max_length=50, default='upwork')
    
    # Marketplace metrics
    marketplace_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    marketplace_score = models.IntegerField(default=0)
    
    # FairFound calculated metrics
    fairfound_score = models.IntegerField(default=0)
    
    # Detailed metrics for comparison
    jobs_completed = models.IntegerField(default=0)
    on_time_percentage = models.IntegerField(default=0)
    response_time_hours = models.IntegerField(default=0)
    rehire_rate = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fairfound_score']

    def __str__(self):
        return f"{self.name} - {self.specialty}"

    def calculate_fairfound_score(self):
        """Calculate FairFound score using weighted equation."""
        score = (
            (self.marketplace_rating * 10) +
            (self.on_time_percentage * 0.3) +
            (min(self.jobs_completed, 200) * 0.1) +
            (self.rehire_rate * 0.2) +
            (max(0, 24 - self.response_time_hours) * 0.5)
        )
        self.fairfound_score = int(min(100, score))
        return self.fairfound_score
