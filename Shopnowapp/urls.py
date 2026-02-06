from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from Shopnowapp import views



urlpatterns = [
    
    path('admin/', admin.site.urls),

    # Home Page
    path('',views.home),

    #register
    path('register', views.register_user, name='register'),

    #login
    path('login', views.login_user, name='login'),

    #logout
    path('logout',views.logout_user, name='logout'),

    path('forgot_pass', views.forgot_pass, name='forgot_pass'),

    path('profile', views.profile, name='profile'),

    path('product/<int:pid>/', views.product_info,name='product_info'),

    path('cart/',views.cart,name='cart'),

    path('orders', views.my_orders, name='order'),

    path('about',views.about, name='about'),

    path('contact',views.contact,name='contact'),

    path('policy', views.policy, name='policy'),

    path('feedback', views.feedback, name='feedback'),


    # For Cart.html
    
    path("add_to_cart/", views.add_to_cart, name="add_to_cart"),
    
    path("update_cart/", views.update_cart, name="update_cart"),

    path('update_quantity/<int:product_id>/<str:action>/', views.update_quantity, name='update_quantity'),

    #storing customer data
    path('place_order/', views.place_order, name='place_order'),

    path('make_payment/',views.make_payment, name='make_payment'),

    #payment handling
    path("payment_done/", views.payment_done, name="payment_done"),


    # other URLs

    path('get_cart/', views.get_cart, name='get_cart'),

    path('search/',views.searchfilter,name='searchfilter'),

    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_cart'),

    path('category/<int:id>/', views.all_products, name='all_products'),
    
    path('catfilter/<int:category_id>/', views.catfilter, name='catfilter'),

    path('login_check',views.login_check),

    path('delete_order_item/<int:item_id>', views.delete_order_item, name='delete_order_item'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)