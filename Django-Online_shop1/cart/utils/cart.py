from shop.models import Product

CART_SESSION_ID = 'cart'




class Subject:
    def __init__(self):
        self._observers = []  

    def add_observer(self, observer):
        """إضافة مراقب إلى القائمة"""
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        """إزالة مراقب من القائمة"""
        self._observers.remove(observer)

    def notify_observers(self):
        """إعلام المراقبين بأي تغيير"""
        for observer in self._observers:
            print("Notifying observers:", self._observers)
            observer.update(self)


        
# class Cart:
#     def __init__(self, request):
#         self.session = request.session
#         self.cart = self.add_cart_session()
class Cart(Subject):
    def __init__(self, request):
        super().__init__()
        self.session = request.session
        self.cart = self.add_cart_session()
        self.notifications = []  


    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['total_price'] = int(item['price']) * int(item['quantity'])
            yield item

    def add_cart_session(self):
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        return cart

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        self.cart.get(product_id)['quantity'] += quantity
        self.save()
        self.notifications.append(f"added {quantity} from {product.name} to cart")
        print(self.notifications)  # طباعة الإشعارات للتأكد
        self.notify_observers() 
        


    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
            self.notifications.append(f"{product.name} has been removed from cart")
            self.notify_observers()  
            

    def save(self):
        self.session.modified = True
       

    def get_total_price(self):
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()
        self.notifications.append("cart cleared")
        self.notify_observers()  
    
    def get_notifications(self):
        return self.notifications