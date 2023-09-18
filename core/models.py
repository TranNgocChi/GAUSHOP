from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime, timezone

# Create your models here.

UserDjango = get_user_model()

class User(models.Model):
    customer = models.ForeignKey(UserDjango, on_delete=models.CASCADE,default='')
    phone = models.CharField(max_length=200, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    town = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.customer.username
    
class new(models.Model):
    post_by = models.ForeignKey(User, on_delete=models.CASCADE, null= True)
    post_date = models.DateTimeField( auto_now_add=True)
    post_content = models.TextField()
    img = models.ImageField(upload_to='news-img',null = True)
    title = models.TextField()
    
    class Meta:
        db_table = "news"
    
    def __str__(self):
        return f"Post by {self.post_by.customer.username} - {self.title}"
    
class Voucher(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expiration_date = models.DateField()
    quantity = models.IntegerField()

    def is_valid(self):
        return self.expiration_date >= timezone.now().date() and self.quantity > 0
    
    def __str__(self):
        return f"Voucher until (Expiration Date: {self.expiration_date.strftime('%Y-%m-%d')})"

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.CharField(max_length=150)
    quantity = models.IntegerField()
    img = models.ImageField(upload_to='product-img', null = True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    voucher = models.ManyToManyField(Voucher, blank=True)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)

    class Meta:
        db_table = 'product'

    def __str__(self):
        return self.name

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    

    class Meta:
        db_table = 'cart'
        
    def cart_total(self):
        self.total = self.quantity * (self.product.price - self.product.discount)

    def voucher(self):
        total_discount = 0
        for voucher in self.product.voucher.all():
            if voucher.is_valid():
                total_discount += voucher.discount_amount
        return total_discount
    
    def __str__(self):
        return 'Cart Of ' + self.customer.customer.username
    
class StatusOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    content = models.CharField(max_length=200, default='Waiting For Confirmation')

    class Meta:
        db_table = 'StatusOrder'

    def __str__(self):
        return self.content
    
class Ordered(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    customer = models.ForeignKey(User, on_delete=models.CASCADE , default=None)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateField(null=True, blank=True)

    country = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    district = models.CharField(max_length=200, null=True, blank=True)
    town = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    
    class Meta:
        db_table = 'ordered'
    
    def __str__(self):
        return "Ordered Of " + self.customer.customer.username
    
class OrderItem(models.Model):
    code = models.UUIDField(primary_key=True, default=uuid.uuid4)
    order = models.ForeignKey(Ordered, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.ForeignKey(StatusOrder, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'order_item'
        
    def __str__(self):
        return "Item Ordered Of " + self.product.name 
    
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    product = models.ForeignKey(Product, related_name="comments", on_delete=models.CASCADE)
    commentor = models.ForeignKey(UserDjango, on_delete=models.CASCADE, default=None)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment'
    
    def __str__(self):
        return "Comment of " + self.commentor.username + " in " + self.product.name
    
class Liked(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'liked'

    def __str__(self):
        return self.customer.customer.username + " liked " + self.product.name
    
