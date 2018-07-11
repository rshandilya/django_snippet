# MODELS SNIPPETS

##### UNIQUE TOGETHER  #####
class MyModel(models.Model):
  field1 = models.CharField(max_length=50)
  field2 = models.CharField(max_length=50)

  class Meta:
    unique_together = ('field1', 'field2',)
