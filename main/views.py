from urllib import request
from urllib.request import Request
from django.shortcuts import render

from django.http import JsonResponse

from django.http import HttpResponse

from main.models import Book,Review,Cart,CartItems,Wishlist,Profile

from django.shortcuts import get_object_or_404,redirect

from django.views import View

from main.form import ReviewForm,RegisterForm,LoginForm,ProfileUpdateForm,UserUpdateForm

from django.contrib.auth.forms import PasswordChangeForm

from django.urls import reverse_lazy

from django.contrib.auth import login,logout,authenticate,update_session_auth_hash

from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import TemplateView,UpdateView

from django.contrib import messages
from django.core.paginator import Paginator

from django.views.generic import ListView

from django.db.models import Q


from .models import Cart, Order, OrderItems

from django.contrib import messages

from django.views.generic import TemplateView
from django.shortcuts import render, reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings


# from django.contrib.auth.views import LoginView

# Create your views here.


class RegisterView(View):

    def get (self,request,*args,**kwargs):

        form = RegisterForm()

        return render(request,'main/registration.html',{'form':form})
    
    def post (self,request):

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request,user)

            return redirect('book_list')
        
        return render(request,'main/registration.html',{'form':form})
    
class LoginView(View):

    def get (self,request):

        form = LoginForm()

        return render(request ,'main/login.html',{'form':form})
    
    def post(self , request , *args , **kwargs):

        form = LoginForm(request,data=request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username,password=password)
            if user is not None:

                login(request , user)

                print('aythentication succesfull')

                return redirect('book_list')
            else:
                print('oombi')
            
                return render (request , 'main/login.html',{'form':form,'error':'invalid credentioal'})
        print('veendum oombi')
        return render (request , 'main/login.html',{'form':form,'error':'invalid credentioal'})



   
class LogoutView(View):

    def get(self,request):

        logout(request)

        return redirect('login')


class BookListView(View):
    def get(self, request):

        query = request.GET.get('q', '')  # Get search query
        
        books = Book.objects.filter(title__icontains=query) if query else Book.objects.all()

        paginator = Paginator(books, 6)  # Show 6 books per page
        
        page_number = request.GET.get('page')
        
        page_obj = paginator.get_page(page_number)

        return render(request, 'main/book_list.html', {'books': page_obj, 'query': query})


    


class BookDetailView(View):

    def get(self,request,book_id):

        book = get_object_or_404(Book, id = book_id)

        reviews = Review.objects.filter(book=book)

        form = ReviewForm()

        return render(request, 'main/book_detail.html',{'book':book,'reviews':reviews , 'form':form})
    
    def post(self,request,book_id,*args,**kwargs):

        book = get_object_or_404(Book,id=book_id)

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit = False)

            review.book = book

            review.user = request.user

            review.save()

            return redirect('book_detail',book_id = book.id)
        
        reviews = Review.objects.filter(book = book)

        return render(request,'main/book_detail.html',{'book':book,'reviews':reviews,'form':form})
    



    
class AddToCartView(View):

    
    def post(self, request,*args,**kwargs):

        if not request.user.is_authenticated:

            messages.warning(request, "You need to log in to add items to your cart.")
           
            return redirect(request.META.get('HTTP_REFERER', 'books'))

        book_id = request.POST.get('book_id')

        # print('book kittiii',book_id)

        book = get_object_or_404(Book, id= book_id)

        # print('book kand',book_id)


        cart , created = Cart.objects.get_or_create(user=request.user)

        # print('cart',cart)

        cart_item , created = CartItems.objects.get_or_create(cart=cart,book=book)

        if not created:

            cart_item.quantity +=1

        cart_item.save()

        # print('cartil kerin',cart_item.book.title)

        return redirect('book_list')
    


class ViewCartView(LoginRequiredMixin,View):

    def get(self,request,*args,**kwargs):

        try:

            cart = Cart.objects.get(user=request.user)

            cart_items = CartItems.objects.filter(cart = cart)

            total_price = 0

            for item in cart_items:
                
                item.total = item.book.price * item.quantity

                total_price += item.total

            return render(request,'main/view_cart.html',{

                'cart':cart,
                'cart_items':cart_items,
                'total_price':total_price,
            })
        
        except Cart.DoesNotExist:

            return render(request,'main/view_cart.html',{

                'cart_items':[],
                'total_price':0
            })


class UpdateCartItemView(LoginRequiredMixin,View):

    def post(self,request,item_id):

        cart_item = get_object_or_404(CartItems,id = item_id, cart__user = request.user)

        quantity = int(request.POST.get('quantity',1))

        if quantity > 0 :
            cart_item.quantity = quantity

            cart_item.save()

        else:
            cart_item.delete()

        return redirect('view_cart')
    


class ClearCartView(LoginRequiredMixin,View):

    def post(self,request,*args,**kwargs):

        cart = Cart.objects.filter(user = request.user).first()

        if cart:

            cart.cartitems_set.all().delete()

        return redirect ('view_cart')
    

class CartCountView(View):

    
    def get(self, request, *args, **kwargs):
    
        if request.user.is_authenticated:
    
            cart_count = request.user.cart.items.count() 
    
        else:
    
            cart_count = 0
    
        return JsonResponse({"cart_count": cart_count})


class CheckoutView(TemplateView):
    template_name = "checkout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_price =0
        total_price = 0
        for cart_item in CartItems:
            total_price += cart_item.book.price * cart_item.quantity

        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": total_price,
            "currency_code": "USD",
            "item_name": "Book Purchase",
            "invoice": "INV-1001",  # You can generate a unique ID
            "notify_url": self.request.build_absolute_uri(reverse('paypal-ipn')),
            "return_url": self.request.build_absolute_uri(reverse('payment_done')),
            "cancel_return": self.request.build_absolute_uri(reverse('payment_canceled')),
        }
        
        context["paypal_form"] = PayPalPaymentsForm(initial=paypal_dict)
        return context

    

class PaymentSuccessView(TemplateView):
    template_name = "payment_done.html"

class PaymentCancelView(TemplateView):
    template_name = "payment_canceled.html"

class OrderSuccessView(TemplateView):
    template_name = 'main/order_success.html'



class OrderHistoryView(LoginRequiredMixin,View):

    def get(self,request,*args,**kwargs):

        orders = Order.objects.filter(user = request.user).order_by('-created_date')

        return render(request,'main/order_history.html',{'orders': orders})
    

class ProfileView(LoginRequiredMixin,TemplateView):
  
  def get(self, request, *args, **kwargs):
        
        profile, created = Profile.objects.get_or_create(user=request.user)
       
        orders = Order.objects.filter(user=request.user)  # Fetch order history

        return render(request, 'main/profile.html', {

            'profile': profile,
            'orders': orders
        })


class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'main/edit_profile.html'

    def get(self, request, *args, **kwargs):
        profile, created = Profile.objects.get_or_create(user=request.user)
        user_form = UserUpdateForm(instance=request.user)  # User form for username update
        profile_form = ProfileUpdateForm(instance=profile)  

        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form
        })

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.username = user.first_name  # Set first name as username
            user.save()

            profile_form.save()

            return redirect('profile')

        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form
        })


class ChangePasswordView(LoginRequiredMixin,View):

    def get(self,request,*args,**kwargs):

        form = PasswordChangeForm(user=request.user)
        
        return render(request , 'main/change_password.html',{'form':form})
    
    def post(self,request):

        form = PasswordChangeForm(user = request.user , data=request.POST)

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(request,user)

            messages.success(request,"your password was succesfully updated !")

            return redirect('login')
        
        else :

            messages.error(request,'please correct the errors below.')

        return render(request,'main/change_password.html',{'form':form})



class WishlistView(LoginRequiredMixin,View):

    def get(self,request,*args,**kwargs):

        whishlist,created = Wishlist.objects.get_or_create(user=request.user)

        return render(request,'main/wishlist.html',{'wishlist':whishlist})
    

class AddToWishlistView(LoginRequiredMixin,View):
    
    def post(self,request,book_id):

        wishlist,created = Wishlist.objects.get_or_create(user=request.user)

        book = get_object_or_404(Book,id=book_id)

        wishlist.books.add(book)

        return redirect('wishlist')
    

class RemoveFromWishlistView(LoginRequiredMixin,View):

    def post(self,request,book_id):

        wishlist = Wishlist.objects.get(user=request.user)

        book = get_object_or_404(Book , id=book_id)

        wishlist.books.remove(book)

        return redirect('wishlist')
    

class MoveToCartView(LoginRequiredMixin,View):

    def post(self,request , book_id,*args,**kwargs):

        book = get_object_or_404(Book,id=book_id)

        cart,created = Cart.objects.get_or_create(user = request.user)

        cart_item, created = CartItems.objects.get_or_create(cart = cart , book=book)

        if not created :

            cart_item.quantity +=1

            cart_item.save()

        wishlist = Wishlist.objects.get(user=request.user)

        wishlist.books.remove(book)

        return redirect('view_cart')





class SearchView(ListView):
    model = Book
    template_name = 'main/search_results.html'
    context_object_name = 'result'

    def get_queryset(self):
        query = self.request.GET.get('query', '').strip()
        if query:
            return Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
        return Book.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', '')

        # DEBUGGING: Print context to check if data exists
        print("DEBUG: Context Data:", context)

        return context  # ✅ FIXED: Must return a dictionary, not HttpResponse


    