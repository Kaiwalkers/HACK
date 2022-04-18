from django.db import models


class Genre(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True)
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    price = models.IntegerField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='movies')
    name = models.CharField(max_length=125)
    description = models.TextField()
    year = models.IntegerField()
    image1 = models.URLField()
    video = models.URLField()

    def __str__(self):
        return self.name



#       "id": 23,
#       "price": 25,
#       "type": "comedy"
#     },
#     {
#       "name": "Mean Girls",
#       "description": "Cue at heng for Aaron Samuels, the ex-boyfriend of alpha Plastic Regina George.",
#       "year": 2004,
#       "image1": "https://i.pinimg.com/736x/26/32/dc/2632dce24165e8f4f0925609c4c37779.jpg",
#       "video":