from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Question(models.Model):
    """Question model map"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=10000)
    # content = models.TextField(null=True, blank=True)
    content = RichTextField()
    likes = models.ManyToManyField(User, related_name='question_post')
    date_create = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """return a string format of the user and the relative question"""
        user_name = self.user.username
        return f'{user_name} - Question'

    def get_absolute_url(self):
        """interconnect the question url"""
        return reverse('soac_base:question-detail', kwargs={'pk':self.pk})

    def total_likes(self):
        """return a total likes on the relative question"""
        return self.likes.count()

class Answer(models.Model):
    """Question model map relative to Question"""
    question = models.ForeignKey(Question, related_name="answer", on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    body = RichTextField()
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        """return the title of the question and it's user"""
        q_title = self.question.title
        q_user = self.question.user
        return f'{q_title} - {q_user}'

    def get_absolute_url(self):
        """return url"""
        return reverse('soac_base:question-detail', kwargs={'pk':self.pk})

    def save(self, *args, **kwargs):
        """ function that saves the instances """
        super().save(*args, **kwargs)
