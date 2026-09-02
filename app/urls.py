from django.urls import path
from .import views



urlpatterns = [
 path("",views.home , name='home'),
 path("reg/",views.user_creation, name='user'),
 path('log/',views.loginform, name='log'),
 path('logout/',views.logout_view,name='out'),
 path('add/<int:id>',views.Addcart,name='add'),  
 path('cart/',views.view_cart,name='cart'),
 path('details/<int:id>',views.product_details,name='all'),
 path('order/',views.previous_orders,name='order'),
 path('buy/<int:id>',views.buy_now , name='buy'),
 path('delete/<int:id>',views.dlt,name='dlt'),
 path('add/<int:id>',views.add, name='plus'),
 path('success/<int:id>',views.success,name='success'),
 path('cancel/',views.cancel,name='cancel'),
]




















