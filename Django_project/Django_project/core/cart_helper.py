from cartapp.models import Products


def add_to_cart_helper(request, product_id):
    product = Products.objects.get(id=product_id)
    cart= request.session.get('cart', {})
    # print(request.session['cart'])
    if str(product_id) in cart:
        cart[str(product_id)] ['image'] = str(product.image)
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {'id':product.pk,'name': product.product_name,'price':product.price,'quantity':1, 'image':str(product.image)}
    request.session['cart'] = cart 
    return request.session['cart']


def remove_from_cart_helper(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart
    return request.session['cart']\
    
def decrement_cart(request, product_id):
    product = Products.objects.get(id=product_id)
    cart= request.session.get('cart', {})
    # print(request.session['cart'])
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] -= 1
    request.session['cart'] = cart 
    return request.session['cart']


