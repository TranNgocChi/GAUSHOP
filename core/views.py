from decimal import Decimal
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import render,redirect, get_object_or_404,HttpResponse
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from .models import *
from django.contrib.auth import login, authenticate, logout
from django.utils import timezone
from datetime import datetime
import random, requests


# Create your views here.

def check(request):
    groups = User.objects.all()
    context={
        'groups': groups,
    }
    return render(request, "check.html", context)

def loginUser(request):
    if request.user.is_authenticated:
        user = User.objects.get_or_create(customer_id = request.user.id)
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, "login.html")

def registerUser(request):
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        request.session['register_data'] ={
            'email':email,
            'username':username,
            'password':password1,
        }
        errorList =[]
        UserDjango = get_user_model()
        check_email = UserDjango.objects.filter(email = email)
        if check_email:
            errorList.append('The Email already exists')
        check_username = UserDjango.objects.filter(username = username)
        if check_username:
            errorList.append('The User already exists')
        if password1 != password2:
            errorList.append('Incorrect Password')
        if errorList:
            return render(request,'register.html',{'errors':errorList})
        else:
            otp = str(random.randint(100000,999999))
            request.session['otp'] = otp
            
            html_content = render_to_string('activation_email.html',{
                'username':username,
                'otp':otp,
            })
            send_mail(
                'OTP Verification for Your Account',
                '',
                'no-reply@shopcenter.com',
                [email,],
                html_message= html_content,
                fail_silently=False,
            )
            return redirect('verify_otp')           
    return render(request, "register.html")

def verify_otp(request):
    if request.method == "POST":
        otp = request.POST.get('otp')
        otp_saved = request.session['otp']
        if otp != otp_saved:
            return render(request,'activation_email_sent.html',{'error':'Incorrect OTP'})
        else:
            register_data = request.session['register_data']
            username = register_data['username']
            email = register_data['email']
            password = register_data['password']
            UserDjango = get_user_model()
            user = UserDjango.objects.create_user(username = username, email = email)
            user.set_password(password)
            user.save()
            user_save = User(customer = user)
            user_save.save()
            return render(request,'activation_success.html')
    return render(request,'activation_email_sent.html')
                
            
            

def logoutUser(request):
    logout(request)
    return redirect('index')

def navbar(request):
    current_path = request.path

    context = {
        'current_path':current_path,
    }
    return render(request, "navbar.html", context)

def index(request):
    all_products = Product.objects.all()
    if len(all_products) >0:
        product_of_month = random.choice(list(all_products))
    else:
        product_of_month = None
    if len(all_products) >= 3:
        random_products = random.sample(list(all_products), 3)
    else:
        random_products = list(all_products)
        
    context = {
        'more_products': random_products,
        'product_of_month': product_of_month
    }
    return render(request, "index.html", context)

def search(request):
    search = str(request.GET.get("search"))
    if search:
        product = Product.objects.all()
        product_search =[]
        for p in product:
            if search.lower() in str(p.name).lower():
                product_search.append(p)
        paginator = Paginator(product_search,6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        check = True
        if not product_search:
            check = False
        context = {
            'page_obj':page_obj,
            'paginator':paginator,
            'page_number':page_number,
            'check': check
        }
        return render(request, "shop.html", context)
    return redirect("shop")

def shop(request):
    products = Product.objects.all()
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    check = True
    if not products:
        check = False
    context = {
        'page_obj': page_obj,
        'paginator':paginator,
        'page_number': page_number,
        'check': check
    }
    return render(request, "shop.html", context)

def about(request):
    context = {
    }
    return render(request, "about.html", context)

def news(request):
    news = new.objects.all()
    if len(news) > 0:
        check = True
    else:
        check = False
    paginator = Paginator(news, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj':page_obj,
        'paginator': paginator,
        'page_number':page_number,
        'check': check,
    }
    return render(request, "news.html", context)

def contact(request):
    if request.method == "POST":
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        admin_mail = "trantrungkien1336@gmail.com"
        send_mail(
            subject,
            f"Name: {name}\nPhone: {phone}\nEmail: {email}\nMessage:\n{message}",
            "no-reply@shopcenter.com",
            [admin_mail],
            fail_silently= False
        )
        
        html_content = render_to_string('contact_email_user.html',{'name':name})
        send_mail(
            'Contact Confirmation',
            '',
            'no-reply@shopcenter.com',
            [email],
            html_message= html_content,
            fail_silently= False
        )
        
    context = {
    }
    return render(request, "contact.html", context)

@login_required
def add_to_cart(request, product_id):
    user = User.objects.get(customer_id  = request.user.id)
    product = Product.objects.get(id=product_id)
    user_cart, created = Cart.objects.get_or_create(customer=user, product=product)
    if not created:
        user_cart.quantity += 1
    if product.quantity > 0:
        product.quantity -= 1
    product.save()
    user_cart.cart_total()
    user_cart.save()
    return HttpResponse(status=200) 


def add_to_favourite(request, product_id):
    user = User.objects.get(customer = request.user)
    try:
        product = Product.objects.get(id = product_id)
        user_liked, created = Liked.objects.get_or_create(customer=user, product=product)
        user_liked.save()
        return JsonResponse({'user_is_logged_in':True}, status=200)
    except Product.DoesNotExist:
        return JsonResponse({"Error": "Not found"}, status=404)

@login_required
def cart(request):
    user = UserDjango.objects.get(id = request.user.id)
    user_id = User.objects.get(customer_id = user.id)
    carts = Cart.objects.filter(customer = user_id)
    discount = 0
    voucher_code = ''
    message = ''
    shipping = 0
    if request.method == "POST":
        for cart in carts:
            quantity_input = int(request.POST.get(f"quantity_{cart.id}",1))
            if quantity_input > cart.product.quantity:
                quantity = 1
                message = 'Quantity unavailable'
            else:
                quantity = quantity_input
            quantity_delta = quantity - cart.quantity
            cart.quantity = quantity
            cart.cart_total()
            cart.product.quantity -= quantity_delta
            cart.product.save()
            cart.save()
        
        voucher = request.POST.get('voucher')
        if voucher:
            vouchers = Voucher.objects.all()
            vouchers_code = [vch.code for vch in vouchers ]
            if voucher in vouchers_code:
                voucher = Voucher.objects.get(code=voucher)
                if voucher.quantity >= 1:
                    voucher.quantity-=1
                    voucher_code = voucher.code
                    discount = voucher.discount_amount
                    voucher.save()
                else:
                    message='Voucher has expired'
                    voucher.delete()
            else:
                message='Voucher not valid'

    if len(carts) > 0:
        check = True
        subtotal = sum(cart.total for cart in carts)
    else:
        check = False
        subtotal = 0
    for cart in carts:
        cart.cart_total()
        cart.save()
    context={
        'carts': carts,
        'check': check,
        'shipping':0,
        'subtotal': subtotal,
        'voucher':discount,
        'message':message,
        'all_total': subtotal + 0 - discount
    }
    request.session['voucher_discount'] = str(discount)
    request.session['voucher_code'] = str(voucher_code)
    return render(request, "cart.html", context)

@login_required
def buyNow(request,product_id):
    product = Product.objects.get(id=product_id)
    discount = 0
    voucher_code = '0'
    message=''
    if request.method == "POST":
        quantity_input = int(request.POST.get(f"quantity_{product.id}",1))
        if quantity_input > product.quantity:
            quantity = 1
            message = 'Quantity unavailable'
        else:
            quantity = quantity_input
            
        voucher = request.POST.get('voucher')
        if voucher:
            try:
                voucher = Voucher.objects.get(code = request.POST.get('voucher'))
                if voucher.quantity >= 1: 
                    voucher.quantity-=1
                    discount = voucher.discount_amount
                    voucher_code = voucher.code
                    voucher.save()
                elif voucher.quantity <= 0:
                    voucher.delete()
                    message='Voucher has expired'
            except:
                voucher=0
                message='Voucher not valid'
    else:
        quantity = 1
    request.session['quantity'] = quantity
    shipping = 0
    total = Decimal(product.price) * int(quantity) - Decimal(product.discount)
    
    
    context={
        'product': product,
        'shipping': shipping,
        'quantity': quantity,
        'total':total,
        'subtotal':total,
        'voucher':discount,
        'message':message,
        'all_total': Decimal(total) + Decimal(shipping) - Decimal(discount),
    }
    request.session['product_id'] = str(product.id)
    request.session['shipping'] = str(shipping)
    request.session['total'] = str(total)
    request.session['subtotal'] = str(total)
    request.session['voucher_discount'] = str(discount)
    request.session['voucher_code'] = str(voucher_code)
    request.session['all_total'] = str(total + shipping - Decimal(discount))
    return render(request, "buy_now.html", context)

def checkout_buynow(request):
    product = Product.objects.get(id = request.session['product_id'])
    user = UserDjango.objects.get(id = request.user.id)
    user_id = User.objects.get(customer_id = user.id)
    context={
        'user': user,
        'carts': [product],
        'shipping':request.session['shipping'],
        'subtotal': request.session['subtotal'],
        'voucher':request.session['voucher_discount'],
        'all_total': request.session['all_total'],
    }
    if request.method =="POST":
        check_list =dict()
        check_list['name'] = request.POST.get('name')
        check_list['email'] = request.POST.get('email')
        check_list['phone'] = request.POST.get('phone')
        check_list['country'] = request.POST.get('country')
        check_list['city'] = request.POST.get('city')
        check_list['district'] = request.POST.get('district')
        check_list['town'] = request.POST.get('town')
        check_list['location'] = request.POST.get('location')
        bill = request.POST.get('bill')
        errorList =[]
        for item in check_list:
            if check_list[item] == '':
                errorList.append(f'Enter your Billing Address: {item}')
                context['errorList'] = errorList
                return render(request,"checkout.html",context)
        order = Ordered.objects.create(customer = user_id,total_amount=0, date=timezone.now())
        discount = float(request.session['voucher_discount'])
        
        order_item = OrderItem.objects.create(
            order = order,
            product = product,
            quantity = request.session['quantity'],
            total = float(request.session['total']),
            shipping = context['shipping'],
        )
        order_item.save()
        order.subtotal += order_item.total
        order.shipping = context['shipping']
        order.total_amount = order.subtotal + float(order.shipping) - discount
        order.save()
        product.quantity -= int(request.session['quantity'])
        product.save()
        request.session['id_ordered'] = str(order.id)
        return redirect('orderSuccess')
            
    return render(request, "checkout.html",context)

def singleNews(request, newId):
    n = new.objects.get(id = newId)
    news = new.objects.all()
    news = list(news)
    random.shuffle(news)    
    context = {
        'new':n,
        'news':news[:6]
    }
    return render(request, "single-news.html",context)

def productDetail(request, productId):
    product = get_object_or_404(Product, id = productId)
    all_products = Product.objects.exclude(pk=productId)
    if len(all_products) >= 3:
        random_products = random.sample(list(all_products), 3)
    else:
        random_products = list(all_products)
        
    if request.method == "POST":
        content = request.POST['comment']
        comment = Comment(product=product,commentor=request.user ,body=content, date=timezone.now())
        comment.save()
        return redirect(request.build_absolute_uri())

    comments = Comment.objects.filter(product=product).order_by('-date')
    quantity_comments = comments.count()
    context = {
        'quantity_comments':quantity_comments,
        'comments': comments,
        'product': product,
        'more_products': random_products,
    }
    return render(request, "product-detail.html",  context)

def checkout(request):
    user = UserDjango.objects.get(id = request.user.id)
    user_id = User.objects.get(customer_id = user.id)
    carts = Cart.objects.filter(customer_id = user_id)
    if len(carts) > 0:
        check = True
        shipping = 0
        subtotal = sum(cart.total for cart in carts)
        error = ''
    else:
        check = False
        shipping = 0
        subtotal = 0
        error = "Cannot check out,your cart is Empty!"
        
    discount = float(request.session['voucher_discount'])
    context={
        'user':request.user,
        'carts': carts,
        'check': check,
        'shipping':shipping,
        'subtotal': subtotal,
        'voucher':discount,
        'all_total': float(subtotal) + shipping - discount,
        'error': error
    }
    if error:
        return render(request,'cart.html',context)
    if request.method == "POST":
        check_list =dict()
        check_list['name'] = request.POST.get('name')
        check_list['email'] = request.POST.get('email')
        check_list['phone'] = request.POST.get('phone')
        check_list['country'] = request.POST.get('country')
        check_list['city'] = request.POST.get('city')
        check_list['district'] = request.POST.get('district')
        check_list['town'] = request.POST.get('town')
        check_list['location'] = request.POST.get('location')
        
        bill = request.POST.get('bill')
        errorList =[]
        for item in check_list:
            if check_list[item] == '':
                errorList.append(f'Enter your : {item}')
                context['errorList'] = errorList
                return render(request,"checkout.html",context)
        order = Ordered.objects.create(
            customer = user_id,total_amount=0, date=timezone.now(),
            country=request.POST.get('country'),
            city=request.POST.get('city'),
            district=request.POST.get('district'),
            town=request.POST.get('town'),
            location=request.POST.get('location'),
            )
        shipping = 0
        for cart in carts:
            order_item = OrderItem.objects.create(
                order = order,
                product = cart.product,
                quantity = cart.quantity,
                total = cart.total,
                shipping = 0,
            )
            order_item.save()
            order.subtotal += order_item.total
            cart.delete()
        order.shipping = 0
        order.total_amount = float(order.subtotal) + float(order.shipping) - discount
        order.save()
        request.session['id_ordered'] = str(order.id)
        return redirect('orderSuccess')
            
    return render(request, "checkout.html",context)

def forgotPassword_input_email(request):
    if request.method == 'POST':
        email = request.POST['email']
        request.session['email_reset_pass'] = email 
        try:
            UserDjango = get_user_model()
            user = UserDjango.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None:
            otp = random.randint(100000,999999)
            request.session['reset_password_otp'] = otp

            html_content = render_to_string('reset_password_email.html',{
                'username':user.username,
                'otp':otp,
            })
            send_mail(
                'OTP Reset Password for Your Account',
                '',
                'no-reply@shopcenter.com',
                [email,],
                html_message= html_content,
                fail_silently=False,
            )
            return redirect('forgotPassword_2')
    return render(request, "forgot_password.html")

def forgotPassword_ResendOrDone(request):
    if request.method =="POST":
        otp = request.POST.get('otp')
        otp_saved = request.session['reset_password_otp']
        
        if str(otp) == str(otp_saved):
            return redirect('forgotPassword_3')
        else:
            return render(request,"forgot_password_2.html",{'error':"Incorrect OTP"})
    return render(request,"forgot_password_2.html")

def forgotPassword_Reset(request):
    if request.method == "POST":
        password1 = request.POST.get('password1')
        password2 = request.POST.get("password2")
        if password1 == password2:
            UserDjango = get_user_model()
            user = UserDjango.objects.get(email = request.session['email_reset_pass'])
            user.set_password(password1)
            user.save()
            return render(request,"reset_success.html")
        else:
            return render(request,"forgot_password_3.html",{'error':'Incorrect password'})
    return render(request,"forgot_password_3.html")

def orderSuccess(request):
    user = User.objects.get(customer_id = request.user.id)
    ordered = Ordered.objects.get(customer_id = user, id = request.session['id_ordered'])
    orders = OrderItem.objects.filter(order_id = ordered)
    context = {
        'ordered': ordered,
        'item_ordereds': orders,
        'vourcher': request.session['voucher_discount']
    }
    return render(request,"order_success.html",context)

def remove_from_cart(request, product_id):
    user = User.objects.get(customer_id=request.user.id)
    product = get_object_or_404(Product, id=product_id)
    cart_del = get_object_or_404(Cart,product = product, customer = user)
    cart_del.delete()
    return redirect('cart')

def cart_count(request):
    try:
        user = User.objects.get(customer_id = request.user.id)
        carts = Cart.objects.filter(customer_id = user.id)
        context={
            'cart_count':len(carts),
        }
    except:
        context={
            'cart_count':""
        }
    return JsonResponse(context)

def liked(request):
    user = User.objects.get(customer=request.user)
    likes = Liked.objects.filter(customer=user)
    context = {
        'likes':likes,
    }
    return render(request, 'liked.html', context)

def remove_from_liked(request, liked_id):
    like = Liked.objects.get(id=liked_id)
    like.delete()
    return redirect('liked')

def voucher(request):
    vouchers = Voucher.objects.all()
    context = {
        'vouchers':vouchers,
    }
    return render(request, 'voucher.html', context)

@login_required 
def order(request):
    user = User.objects.get(customer=request.user)
    ordereds = Ordered.objects.filter(customer=user)
    order_items = []
    check = False

    for ordered in ordereds:
        order_items.extend(OrderItem.objects.filter(order=ordered))
        check = True

    order_items = sorted(order_items, key = lambda x : x.order.date, reverse=True)

    context = {
        'check': check,
        'orderitems': order_items,
    }
    return render(request, 'order.html', context)

@login_required 
def remove_from_orderitem(request, orderitem_id):
    orderitem = OrderItem.objects.get(code=orderitem_id) 
    orderitem.delete()  
    return redirect('order')

@login_required
def profile(request):
    UserDjango = get_user_model()
    user = UserDjango.objects.get(id = request.user.id)
    user_now = User.objects.get(customer_id= user.id)
    if request.method == "POST":
        username = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        country = request.POST.get('country')
        province = request.POST.get('province')
        district = request.POST.get('district')
        town = request.POST.get('town')
        location = request.POST.get('location')

        if username:
            user_now.customer.username = username
        else:
            user_now.customer.username = 'Username is empty'
        if email:
            user_now.customer.email = email
        else:
            user_now.customer.email = 'Email is empty'
        if phone:
            user_now.phone = phone
        else:
            user_now.phone = 'Phone is empty'
        if country:
            user_now.country = country
        else:
            user_now.country = 'Country is empty'
        if province:
            user_now.province = province
        else:
            user_now.province = 'Province is empty'
        if district:
            user_now.district = district
        else:
            user_now.district = 'District is empty'
        if town:
            user_now.town = town
        else:
            user_now.town = 'Town is empty'    
        if location:
            user_now.location = location
        else:
            user_now.location = 'Location is empty'
        user_now.customer.save()
        user_now.save()
        return redirect('profile')
    
    context = {
        'user_now':user_now,
    }
    return render(request, 'profile.html', context)
