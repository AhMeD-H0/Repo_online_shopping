from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from cart.forms import Add2CartForm
from shop.models import Product
from cart.utils.cart import Cart
from django.views.decorators.http import require_POST
from django.contrib import messages
from cart.notification import Notification  

def detail(request):
    cart = Cart(request)
    notification = Notification()  
    cart.add_observer(notification)  
    notification.update(cart) 
    # return render(request, template_name='cart/detail.html', context={'cart': cart})
    return render(request, template_name='cart/detail.html', context={'cart': cart, 'notifications': notification.messages})

   


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = Add2CartForm(request.POST)  
    if form.is_valid():
        data = form.cleaned_data
        cart.add(product=product, quantity=data['quantity'])
    return redirect('cart:detail')
    


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:detail')
