from django.contrib import admin

from main.models import Book,Review,Order

# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = ('title','description','price','published_date')

    search_fields = ('title','auther')

    list_filter = ('published_date',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = ('book','user','rating','created_date')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ('user','total_price','created_date')

