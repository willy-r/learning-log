from django.db import models
from django.contrib.auth import get_user_model


class Topic(models.Model):
    topic_text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    public = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.topic_text


class Entry(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    entry_text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'
        ordering = ['-date_added']

    def __str__(self):
        if len(self.entry_text) <= 50:
            return self.entry_text
        return f'{self.entry_text[:50]}...'

