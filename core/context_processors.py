from .models import Cart, User

def navbar(request):
    try:
        user = User.objects.get(customer_id=request.user.id)
        carts = Cart.objects.filter(customer_id = user.id)
        context={
            'count_cart':len(carts),
        }
    except:
        context ={
            'count_cart':''
        }
    return context