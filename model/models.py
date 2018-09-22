# MODELS SNIPPETS

#### MANYTOMANY FIELD #######
class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')

    def __str__(self):
        return self.name

class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)





##### UNIQUE TOGETHER  #####
class MyModel(models.Model):
  field1 = models.CharField(max_length=50)
  field2 = models.CharField(max_length=50)

  class Meta:
    unique_together = ('field1', 'field2',)
    
#### USE OF PROXY MODEL #######
class MyModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UpperModel(MyModel):
    class Meta:
        proxy = True

    def __str__(self):
        return self.name.upper()

----------------------------------
STORY_TYPES = (
    ('f', 'Feature'),
    ('i', 'Infographic'),
    ('g', 'Gallery'),
)

class Story(models.Model):
    type = models.CharField(max_length=1, choices=STORY_TYPES)
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True, null=True)
    infographic = models.ImageField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    gallery = models.ForeignKey(Gallery, blank=True, null=True)
    
class FeatureStory(Story):
    objects = FeatureManager()
    class Meta:
        proxy = True

class InfographicStory(Story):
    objects = InfographicManager()
    class Meta:
        proxy = True

class GalleryStory(Story):
    objects = GalleryManager()
    class Meta:
        proxy = True

class FeatureManager(models.Manager):
    def get_queryset(self):
        return super(FeatureManager, self).get_queryset().filter(type='f')

class InfographicManager(models.Manager):
    def get_queryset(self):
        return super(InfographicManager, self).get_queryset().filter(type='i')

class GalleryManager(models.Manager):
    def get_queryset(self):
        return super(GalleryManager, self).get_queryset().filter(type='g')

------------------------------------------------------
class MediaAsset(models.Admin):
    type = models.CharField(max_length=5, default='image')
    caption = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)

class Image(MediaAsset):
    objects = ImageManager()
    class Meta:
        proxy = True

class Video(MediaAsset):
    objects = VideoManager()
    class Meta:
        proxy = True

class ImageManager(models.Manager):
    def get_queryset(self):
        return super(ImageManager, self).get_queryset().filter(
            type='image')

class VideoManager(models.Manager):
    def get_queryset(self):
        return super(VideoManager, self).get_queryset().filter(
            type='video')

    def create(self, **kwargs):
        kwargs.update({'type': 'video'})
        return super(VideoManager, self).create(**kwargs)
===========================================================    
    
    
