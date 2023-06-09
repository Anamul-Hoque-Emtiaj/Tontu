from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.home,name='home'),
    path('search',views.search,name='search'),
    path('category-list',views.category_list,name='category-list'),
    path('product-list',views.product_list,name='product-list'),
    path('category-product-list/<int:cat_id>',views.category_product_list,name='category-product-list'),
    path('product/<str:slug>/<int:id>',views.product_detail,name='product_detail'),
    path('filter-data',views.filter_data,name='filter_data'),
    path('load-more-data',views.load_more_data,name='load_more_data'),
    path('add-to-cart',views.add_to_cart,name='add_to_cart'),
    path('cart',views.cart_list,name='cart'),
    path('cart/',views.cart_list,name='cart1'),
    path('delete-from-cart',views.delete_cart_item,name='delete-from-cart'),
    path('update-cart',views.update_cart_item,name='update-cart'),
    path('accounts/signup',views.signup,name='signup'),
    path('accounts/login',views.login,name='login'),
    path('checkout',views.checkout,name='checkout'),
    path('save-review/<int:pid>',views.save_review, name='save-review'),
    # User Section Start
    path('my-dashboard',views.my_dashboard, name='my_dashboard'),
    path('my-orders',views.my_orders, name='my_orders'),
    path('my-orders-items/<int:id>',views.my_order_items, name='my_order_items'),
    # End

    # Wishlist
    path('add-wishlist',views.add_wishlist, name='add_wishlist'),
    path('my-wishlist',views.my_wishlist, name='my_wishlist'),
    path('delete-from-wishlist/<int:id>',views.delete_from_wishlist, name='delete-from-wishlist'),
    # My Reviews
    path('my-reviews',views.my_reviews, name='my-reviews'),
    path('edit-profile',views.edit_profile, name='edit-profile'),
    path('password/',views.password, name='password'),
    path('about-us/',views.about_us, name='about-us'),
    path('accounts/password_change/',views.password_change,name='password_change'),

    path('test/',views.test, name='test'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)