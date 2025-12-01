from django.db import models


class ComparisonHistory(models.Model):
    """Track comparison requests for analytics."""
    
    freelancer1_url = models.URLField()
    freelancer2_url = models.URLField()
    winner_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Comparison histories'
        ordering = ['-created_at']

    def __str__(self):
        return f"Comparison at {self.created_at}"
