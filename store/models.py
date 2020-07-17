from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Customer(models.Model):
     user  = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
     name  = models.CharField(max_length=200,null=True)
     email = models.CharField(max_length=200,null=True)

     def __str__(self):
          return self.name




@receiver(post_save, sender=User)
def create_user_cutomer(sender, instance, created, **kwargs):
     if created:
          Customer.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_cutomer(sender, instance, created, **kwargs):
     instance.customer.save()



class Product(models.Model):
     name    = models.CharField(max_length=200,null=True)
     price   = models.FloatField()
     digital = models.BooleanField(default=False,null=True,blank=True)
     image   = models.ImageField(null=True, blank=True)
     
     def __str__(self):
          return self.name

     #get image url if not then default image fatch
     @property
     def imageURL(self):
          try:
               url = self.image.url
          except:
               url = 'images/placeholder.png'
          return url
     
#cart
class Order(models.Model):
     customer      = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
     date_ordered  = models.DateTimeField(auto_now_add=True)
     complete      = models.BooleanField(default=False)
     trasaction_id = models.CharField(max_length=100,null=True)

     def __str__(self):
          return str(self.id)

     #TOTAL OF CART INCLUDING ALL ITEMS WITH THEIR QUANTITY
     @property
     def get_cart_total(self):
          total = 0
          for item in self.orderitem_set.all():
               total +=item.get_total
          return total
     #TOTAL ORDER ITEMS INCUGDING IDIVIDUAL QUANTITY
     @property
     def get_cart_items(self):
          total_items = 0
          for item in self.orderitem_set.all():
               total_items += item.quantity
          return total_items



class OrderItem(models.Model):
     product    = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
     order      = models.ForeignKey(Order, on_delete=models.SET_NULL,null=True)
     quantity   = models.IntegerField(default=0, null=True, blank=True)
     date_added = models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return self.product.name
     
     #GET IDIVISUAL ITEM TOTAL PRICE WITH MULTIPLING WITH QUANTITY
     @property
     def get_total(self):
          total = self.product.price * self.quantity
          return total

class ShippingAddress(models.Model):
     customer   = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
     order      = models.ForeignKey(Order, on_delete=models.SET_NULL,null=True)
     address    = models.CharField(max_length=200,null=False)
     city       = models.CharField(max_length=200,null=False)
     state      = models.CharField(max_length=200,null=False)
     zipcode    = models.CharField(max_length=200,null=False)
     date_added = models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return f'{self.customer.name}--{self.address}'


