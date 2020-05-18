from django.db import models
from django.contrib.auth import get_user_model


class Topic(models.Model):
    """Model for the topic that the user is learning about."""
    topic_text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    public = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        """Returns the string representation of the topic."""
        return self.topic_text


class Entry(models.Model):
    """Model for an entry of a specific topic."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    entry_text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'
        ordering = ['-date_added']

    def __str__(self):
        """Returns the string representation of the entry."""
        if len(self.entry_text) <= 30:
            return self.entry_text
        return f'{self.entry_text[:30]}...'
