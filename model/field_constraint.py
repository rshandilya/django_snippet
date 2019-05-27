from django.core.validators import MaxValueValidator

class MyModel(models.Model):
    ...
    id_student = models.PositiveIntegerField(primary_key=True, validators=[MaxValueValidator(9999999999)])
    
    
class MyModel(models.Model):
    ...
    id_student = models.CharField(primary_key=True, max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])    
