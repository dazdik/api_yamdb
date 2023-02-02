from django.db import models


class Genres(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return f'{self.name} {self.slug}'


# # Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return f'{self.name} {self.slug}'


class Titles(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()
    rating = models.IntegerField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='category_title',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genres,
        through='GenresTitle'
    )

    class Meta:
        ordering = ['id']


class GenresTitle(models.Model):
    genres = models.ForeignKey(Genres, on_delete=models.CASCADE)
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genres} {self.title}'
