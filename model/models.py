# MODELS SNIPPETS


############## FOREIGNKEY DEFINED USING STRING IN ADVANCE ###########
#products/models.py
from django.db import models

class AbstractCar(models.Model):
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.CASCADE)

    class Meta:
        abstract = True

# profuction/models.py
from django.db import models
from products.models import AbstractCar

class Manufacturer(models.Model):
    pass

class Car(AbstractCar):
    pass



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


########  RELATED MANAGER ##########
from django.db import models

### Other side of ForeignKey relations
class Reporter(models.Model):
    # ...
    pass

class Article(models.Model):
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)

# the methods below will be available on the manager reporter.article_set

## Both side of ManyToManyField relations   
class Topping(models.Model):
    # ...
    pass

class Pizza(models.Model):
    toppings = models.ManyToManyField(Topping)    
    
# the methods below will be available both on topping.pizza_set and on pizza.toppings    

# add(*objs, bulk=True)
>>> b = Blog.objects.get(id=1)
>>> e = Entry.objects.get(id=234)
>>> b.entry_set.add(e) # Associates Entry e with Blog b.

# create(**kwargs)
>>> b = Blog.objects.get(id=1)
>>> e = b.entry_set.create(
...     headline='Hello',
...     body_text='Hi',
...     pub_date=datetime.date(2005, 1, 1)
... )
# No need to call e.save() at this point -- it's already been saved.

# remove(*objs, bulk=True)
>>> b = Blog.objects.get(id=1)
>>> e = Entry.objects.get(id=234)
>>> b.entry_set.remove(e) # Disassociates Entry e from Blog b.

# clear(bulk=True)
>>> b = Blog.objects.get(id=1)
>>> b.entry_set.clear()

# set(objs, bulk=True, clear=False)
>>> new_list = [obj1, obj2, obj3]
>>> e.related_set.set(new_list)
    
    


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

#------------------------------------------------------
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
#===========================================================    
    
##########  SLUGIFY  ##########
from django.db import models
from django.utils.text import slugify
 
 
class Article(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    content = models.TextField()
 
    def __str__(self):
        return self.title
 
    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Article.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)
