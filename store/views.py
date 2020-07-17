from django.shortcuts import render
from .models import Customer, Product, Order, OrderItem, ShippingAddress
from .forms import CustomerForm
from django.contrib.auth.forms import UserCreationForm

def store(request):
     products = Product.objects.all()
     #get login customer
     if request.user.is_authenticated:
          customer = request.user.customer
          # fatch order of login customer
          order = Order.objects.get(customer=customer, complete =False)
          if request.method == "POST":
               product_id = request.POST.get('product')
               product = Product.objects.get(id=product_id)
               try:
                    #here we have fatch orderitem which comes under above product and order both
                    orderitem = OrderItem.objects.get(product = product,order=order)
                    orderitem.quantity+=1
                    orderitem.save()
                    print(orderitem.quantity)
                    print("Try")
               except OrderItem.DoesNotExist:
                    # if order item does not exist we need to create it with quantity 
                    item = OrderItem(product=product,order=order,quantity=1)
                    item.save()
                    print("EX")

          
                    

     context ={
          'products':products
     }
     return render(request,'store/store.html',context)



def cart(request):
     # if cuatomer is logged in
     if request.user.is_authenticated:
          #get login customer
          customer = request.user.customer
          # fatch order of login customer
          order = Order.objects.get(customer=customer, complete =False)
          # fatch all items for order
          items = order.orderitem_set.all()
          #logic of quantity increase and decrease with up and down arrow and if quantity is zero it have to discart from the cart
          
          if request.method == 'POST':
               product_id = request.POST.get('product') 
               product = Product.objects.get(id=product_id) 
               orderitem = OrderItem.objects.get(order=order,product=product)
               if 'btn-inc' in request.POST:
                    
                    orderitem.quantity+=1
                    orderitem.save()
                    
               if 'btn-dec' in request.POST:
                    if orderitem.quantity > 1:
                         orderitem.quantity-=1
                         orderitem.save()
                    else: 
                         orderitem.delete()

     # if customer is not logged in  
     else:
          #no item, if we not passing this we will get 
          items =[]
          #dummy data so we can show 0,0, if customer is not logged in
          order = {'get_cart_total':0,'get_cart_items':0} 
     context ={
          'items': items,
          'order': order
     }
     #logic of quantity increase and decrease with up and down arrow and if quantity is zero it have to discart from the cart
     



     return render(request,'store/cart.html',context)

def checkout(request):
     # Right side of the checkout page logic which is same as cart logic we have to check the customer is logged in or not
     # if cuatomer is logged in
     if request.user.is_authenticated:
          #get login customer
          customer = request.user.customer
          # fatch order of login customer
          order = Order.objects.get(customer=customer, complete =False)
          # fatch all items for order
          items = order.orderitem_set.all()
     # if customer is not logged in  
     else:
          #no item, if we not passing this we will get 
          items =[]
          #dummy data so we can show 0,0, if customer is not logged in
          order = {'get_cart_total':0,'get_cart_items':0} 
     context ={
          'items': items,
          'order': order
     }

     #left side of the checkout page there is a form which submit the shipping address in POST method


     return render(request,'store/checkout.html',context)

def customer_create(request):
     if request.method == 'POST':
          user_form = UserCreationForm(request.POST)
          customer_form = CustomerForm(request.POST)
          if user_form.is_valid() and customer_form.is_valid():
               user_form.save()
               customer_form.save()
     else:
          user_form = UserCreationForm()
          customer_form = CustomerForm()
     context = {
          'user_form':user_form,
          'customer_form': customer_form
     }
     return render(request,'store/customer_create.html',context)
