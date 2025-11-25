from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        self.cart = cart
        
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        if product_id in self.cart:
            self.cart[product_id] += int(product_qty)
        else:
            self.cart[product_id] = int(product_qty)
            
        self.session.modified = True
        
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            current_user.update(old_cart=carty)
        else:
            pass
        
    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        if product_id in self.cart:
            self.cart[product_id] += int(product_qty)
        else:
            self.cart[product_id] = int(product_qty)
            
        self.session.modified = True
        
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            current_user.update(old_cart=carty)
        else:
            pass
         
        
    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True
        else:
            pass
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            current_user.update(old_cart=carty)
        else:
            pass
        
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        cart = self.cart
        cart[product_id] = product_qty
        self.session.modified = True
    
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            current_user.update(old_cart=carty)
        else:
            pass
        
        updated_cart = self.cart
        return updated_cart

    def total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        total = 0
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_on_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
        return total