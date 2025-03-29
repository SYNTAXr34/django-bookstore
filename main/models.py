from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
   
    bio = models.TextField(blank=True)

    location = models.CharField(max_length=100, blank=True)

    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Book(models.Model):

    title = models.CharField(max_length=200)

    author = models.CharField(max_length=200)

    description = models.TextField()

    price = models.DecimalField(max_digits=6 ,decimal_places=2)

    published_date = models.DateField()

    cover_image = models.ImageField(upload_to='book_covers/',blank=True,null=True)

    def __str__(self):
        return self.title
    

class Review(models.Model):

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')

    user = models.ForeignKey(User , on_delete=models.CASCADE)

    rating = models.IntegerField()

    comment = models.TextField()

    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.book.title}'
    

class Cart(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    items = models.ManyToManyField(Book, through= 'CartItems')

    def __str__(self):
        return f'{self.user.username} - Cart'
    

class CartItems(models.Model):

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.book.title} ({self.quantity})'
    

class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    book = models.ManyToManyField(Book,through='OrderItems')

    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    created_date = models.DateTimeField(auto_now_add=True)

    def calculate_total_price(self):

        total = sum(item.book.price * item.quantity for item in self.orderitems_set.all())

        self.total_price = total

        self.save()

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'
    

class OrderItems(models.Model):

    order = models.ForeignKey(Order , on_delete=models.CASCADE, related_name='order_items')

    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    quantity = models.PositiveBigIntegerField()

    

    def __str__(self):
        return f'{self.book.title} ({self.quantity})'


class Wishlist(models.Model):

    user = models.ForeignKey(User , on_delete=models.CASCADE)

    books = models.ManyToManyField(Book)

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username}'s Wishlist"