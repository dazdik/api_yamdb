from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from api.models import Title

User = get_user_model()

CROP_LEN_TEXT = 30


# class Titles(models.Model):
#     name = models.CharField(max_length=256)
#     year = models.IntegerField()
#     description = models.TextField()
#     rating = models.IntegerField()
#     category = models.CharField(max_length=256)
#     genre = models.CharField(max_length=256)

#     def __str__(self):
#         return self.name[:CROP_LEN_TEXT]

class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(10),
    ])
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )
    title = models.CharField(max_length=128)
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            ),
        ]
    
    def __str__(self):
        return self.text[:CROP_LEN_TEXT]


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:CROP_LEN_TEXT]
