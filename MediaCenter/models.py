from django.db import models

class Song(models.Model):
    filename = models.CharField(max_length=30)
    directory = models.CharField(max_length=70)
    url = models.CharField(max_length=60)
    artist = models.CharField(max_length=30)
    album = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    # Should some sort of limit be set? can it?
    track_number = models.IntegerField()

    def __unicode__(self):
        return self.title
    
