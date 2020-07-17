from django.urls import path
from .views import store, cart, checkout, customer_create

from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
     path('',store,name='store'),
     path('cart/',cart,name='cart'),
     path('checkout/',checkout,name='checkout'),
     path('customer_create/',customer_create,name='customer-create')
     
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)