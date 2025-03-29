from django.contrib import admin
from django.urls import path,include
from main.views import BookListView, BookDetailView, AddToCartView, ViewCartView, RegisterView, LoginView, LogoutView ,CheckoutView
from main.views import UpdateCartItemView,ClearCartView,OrderSuccessView,OrderHistoryView,ProfileView,SearchView,CartCountView
from main.views import ChangePasswordView,WishlistView,AddToWishlistView,RemoveFromWishlistView,MoveToCartView,ProfileUpdateView, PaymentSuccessView, PaymentCancelView
from paypal.standard.ipn import views as paypal_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', BookListView.as_view(), name='home'),
    path('books/', BookListView.as_view(), name='book_list'),
    path('book/<int:book_id>/', BookDetailView.as_view(), name='book_detail'),
    path('cart/', ViewCartView.as_view(), name='view_cart'),
    path('add_to_cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('cart/update/<int:item_id>/', UpdateCartItemView.as_view(), name='update_cart_item'),
    path('cart/clear/', ClearCartView.as_view(), name='clear_cart'),
    path('order-success/', OrderSuccessView.as_view(), name='order_success'),
    path('order-history/', OrderHistoryView.as_view(), name='order_history'),
    path('profile/', ProfileView.as_view(), name='profile'),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('wishlist/add/<int:book_id>/', AddToWishlistView.as_view(), name='add_to_wishlist'),
    path('wishlist/remove/<int:book_id>/', RemoveFromWishlistView.as_view(), name='remove_from_wishlist'),
    path('wishlist/move_to_cart/<int:book_id>/', MoveToCartView.as_view(), name='move_to_cart'),
    path('search/', SearchView.as_view(), name='search_results'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='edit_profile'),
    path('cart/count/', CartCountView.as_view(), name='cart-count'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment-done/', PaymentSuccessView.as_view(), name='payment_done'),
    path('payment-cancelled/', PaymentCancelView.as_view(), name='payment_canceled'),





]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)