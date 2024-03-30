from django.db import models

# Create your models here.
class Product(models.Model): 
    name = models.CharField(max_length=50) 
    description = models.TextField() 
    price = models.DecimalField(max_digits=5, decimal_places=2) 
    image = models.ImageField(upload_to='products/%y/%m/%d/') 
    # category = models.ForeignKey(Categories, on_delete=models.PROTECT) 
    active=models.BooleanField(default=True)
    stock = models.IntegerField(default=0)


    def __str__(self): 
        return self.name
