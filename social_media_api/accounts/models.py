from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    # Only define 'following', and Django will automatically create the reverse relation
    following = models.ManyToManyField(
        'self',
        symmetrical=False,  # Ensures "A follows B" doesn't mean "B follows A"
        related_name='followers',  # 'followers' is now the reverse relation
        blank=True
    )

    def follow(self, user):
        """Follow another user."""
        self.following.add(user)

    def unfollow(self, user):
        """Unfollow a user."""
        self.following.remove(user)

    def __str__(self):
        return self.username
