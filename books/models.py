from django.db import models
from django.contrib.auth.models import User

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=255, default='Unknown Title')
    book_description = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    link = models.URLField(max_length=2000, blank=True, null=True)
    cover_image = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    publication_date = models.CharField(max_length=255, blank=True, null=True)
    rating = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.book_title

    def like_count(self):
        return self.likes.count()

class Comment(models.Model):
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.recommendation.book_title}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recommendation = models.ForeignKey(Recommendation, related_name='likes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'recommendation')

    def __str__(self):
        return f"{self.user.username} likes {self.recommendation.book_title}"
