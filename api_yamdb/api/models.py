from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=False, max_length=50)

    def __str__(self):
        return f'{self.name} {self.slug}'


# # Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return f'{self.name} {self.slug}'


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='category_title',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenresTitle'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['id']


class GenresTitle(models.Model):
    genres = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genres} {self.title}'
