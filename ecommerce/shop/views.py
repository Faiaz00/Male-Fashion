from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.views import View
from . models import Customer, Product, Cart, OrderPlaced
from . forms import CustomerRegistrationForm, LoginForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q,F
from django.http import JsonResponse, Http404
from django.utils.decorators import method_decorator

# Create your views here.
class ProductView(View):
     def get(self, request):
       totalitem = 0
       clothings_hot = Product.objects.filter(category='CH')
       shoe_collection = Product.objects.filter(category = 'SC')
       accessories = Product.objects.filter(category = 'A')
       if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
       return render(request, 'shop/home.html', {'clothings_hot':clothings_hot, 'shoe_collection':shoe_collection,'accessories':accessories,'totalitem':totalitem })

class ProductDetailView(View):
 def get(self, request, pk):
   totalitem = 0
   product = Product.objects.get(pk=pk)
   item_already_in_cart = False
   if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
     item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
   return render(request, 'shop/productdetail.html', {'product':product,'item_already_in_cart': item_already_in_cart, 'totalitem':totalitem})

def add_to_cart(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        user = request.user
        product_id = request.POST.get('prod_id')
        product = get_object_or_404(Product, id=product_id)

        cart_item, created = Cart.objects.get_or_create(user=user, product=product)
        if not created:
            cart_item.quantity = F('quantity') + 1
            cart_item.save()
            cart_item.refresh_from_db()

        return redirect('showcart')

    return redirect('home')
        

def show_cart(request):
  if request.user.is_authenticated:
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 100.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user==user]
    if cart_product:
      for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
        totalamount = amount + shipping_amount
    else:
      return render(request,'shop/emptycart.html')
    return render(request, 'shop/addtocart.html', {'carts':cart, 'totalamount':totalamount, 'amount':amount})
  else:
        return redirect('login')


def buy_now(request):
 return render(request, 'shop/buynow.html')


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
  def get(sef, request):
    form = CustomerProfileForm()
    return render(request, 'shop/profile.html', {'form':form, 'active':'btn-primary'})
  
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        c = Cart.objects.filter(product_id=prod_id, user=request.user).first()
        if c:
            c.quantity = F('quantity') + 1
            c.save()
            c.refresh_from_db()

        amount = 0.0
        shipping_amount = 100.0
        cart_products = Cart.objects.filter(user=request.user)
        for p in cart_products:
            amount += p.quantity * p.product.discounted_price
        totalamount = amount + shipping_amount

        data = {
            'quantity': c.quantity if c else 0,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

  

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        c = Cart.objects.filter(product_id=prod_id, user=request.user).first()
        if c:
            if c.quantity > 1:
                c.quantity = F('quantity') - 1
                c.save()
                c.refresh_from_db()
            else:
                c.delete()
                c = None

        amount = 0.0
        shipping_amount = 100.0
        cart_products = Cart.objects.filter(user=request.user)
        for p in cart_products:
            amount += p.quantity * p.product.discounted_price
        totalamount = amount + shipping_amount

        data = {
            'quantity': c.quantity if c else 0,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        Cart.objects.filter(product_id=prod_id, user=request.user).delete()

        amount = 0.0
        shipping_amount = 100.0
        cart_products = Cart.objects.filter(user=request.user)
        for p in cart_products:
            amount += p.quantity * p.product.discounted_price
        totalamount = amount + shipping_amount

        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)



def post(self, request):
    form = CustomerProfileForm(request.POST)
    if form.is_valid():
        usr = request.user
        name = form.cleaned_data['name']
        division = form.cleaned_data['division']
        district = form.cleaned_data['district']
        thana = form.cleaned_data['thana']
        street_address = form.cleaned_data['street_address']
        zipcode = form.cleaned_data['zipcode']
        reg = Customer(user=usr,name=name, division=division,district=district, thana=thana, street_address=street_address, zipcode=zipcode)
        reg.save()
        messages.success(request, 'Congratulations! Profile Updated Successfully')
        return render(request, 'shop/profile.html', {'form':form, 'active':'btn-primary'})

@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'shop/address.html', {'add':add, 'active':'btn-primary'})

def buy_now(request):
 return render(request, 'shop/buynow.html')

def address(request):
 return render(request, 'shop/address.html')

def orders(request):
 return render(request, 'shop/orders.html')

def checkout(request):
    return render(request, 'shop/checkout.html')


def order_success(request):
    name = request.session.pop('order_name', 'Customer')
    email = request.session.pop('order_email', '')
    return render(request, 'shop/order_success.html', {'name': name, 'email': email})


def shopdetails(request):
      return render (request, 'shop/shop-details.html')

def blog(request):
      return render (request, 'shop/blog.html')

def blogdetails(request):
      return render (request, 'shop/blog-details.html')

def contact(request):
    return render(request, 'shop/contact.html')

def shop(request):
    return render(request, 'shop/shop.html')

def home(request):
    return render(request, 'shop/index.html')



def clothings_category_view(request, category):
    if category not in VALID_CLOTHING_CATEGORIES:
        raise Http404("Category not found")
    
    VALID_CLOTHING_CATEGORIES = {
        'tshirt': 'T-shirt',
        'pant': 'Pant',
        'jacket': 'Jacket',
        'hoodie': 'Hoodie',
    }

    context = {
        'category': VALID_CLOTHING_CATEGORIES[category],
    }
    return render(request, 'shop/clothings_category.html', context)

def tshirt_view(request):
    tshirts = Product.objects.filter(category__iexact='tshirt')
    brand = request.GET.get('brand')
    price = request.GET.get('price')
    query = request.GET.get('q')

    if brand:
        tshirts = tshirts.filter(brand__iexact=brand)

    if price:
        if price == 'below5000':
            tshirts = tshirts.filter(discounted_price__lt=5000)
        elif price == 'below20000':
            tshirts = tshirts.filter(discounted_price__gte=5000, discounted_price__lt=20000)
        elif price == 'below45000':
            tshirts = tshirts.filter(discounted_price__gte=20000, discounted_price__lt=45000)
        elif price == 'below70000':
            tshirts = tshirts.filter(discounted_price__gte=45000, discounted_price__lt=70000)
        elif price == 'above70000':
            tshirts = tshirts.filter(discounted_price__gte=70000)

    if query:
        tshirts = tshirts.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query)
        )

    paginator = Paginator(tshirts, 9)
    page = request.GET.get('page')
    tshirts = paginator.get_page(page)
    return render(request, 'shop/clothings/tshirt.html', {'tshirts': tshirts, 'title': 'T-shirt'})

def pant_view(request):
    pants = Product.objects.filter(category__iexact='pant')
    brand = request.GET.get('brand')
    price = request.GET.get('price')
    query = request.GET.get('q')

    if brand:
        pants = pants.filter(brand__iexact=brand)

    if price:
        if price == 'below5000':
            pants = pants.filter(discounted_price__lt=5000)
        elif price == 'below20000':
            pants = pants.filter(discounted_price__gte=5000, discounted_price__lt=20000)
        elif price == 'below45000':
            pants = pants.filter(discounted_price__gte=20000, discounted_price__lt=45000)
        elif price == 'below70000':
            pants = pants.filter(discounted_price__gte=45000, discounted_price__lt=70000)
        elif price == 'above70000':
            pants = pants.filter(discounted_price__gte=70000)

    if query:
        pants = pants.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query)
        )

    paginator = Paginator(pants, 9)
    page = request.GET.get('page')
    pants = paginator.get_page(page)
    return render(request, 'shop/clothings/pant.html', {'pants': pants, 'title': 'Pant'})

def jacket_view(request):
    jackets = Product.objects.filter(category__iexact='jacket')
    brand = request.GET.get('brand')
    price = request.GET.get('price')
    query = request.GET.get('q')

    if brand:
        jackets = jackets.filter(brand__iexact=brand)

    if price:
        if price == 'below5000':
            jackets = jackets.filter(discounted_price__lt=5000)
        elif price == 'below20000':
            jackets = jackets.filter(discounted_price__gte=5000, discounted_price__lt=20000)
        elif price == 'below45000':
            jackets = jackets.filter(discounted_price__gte=20000, discounted_price__lt=45000)
        elif price == 'below70000':
            jackets = jackets.filter(discounted_price__gte=45000, discounted_price__lt=70000)
        elif price == 'above70000':
            jackets = jackets.filter(discounted_price__gte=70000)

    if query:
        jackets = jackets.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query)
        )

    paginator = Paginator(jackets, 9)
    page = request.GET.get('page')
    jackets = paginator.get_page(page)
    return render(request, 'shop/clothings/jacket.html', {'jackets': jackets, 'title': 'Jacket'})

def hoodie_view(request):
    hoodies = Product.objects.filter(category__iexact='hoodie')
    brand = request.GET.get('brand')
    price = request.GET.get('price')
    query = request.GET.get('q')

    if brand:
        hoodies = hoodies.filter(brand__iexact=brand)

    if price:
        if price == 'below5000':
            hoodies = hoodies.filter(discounted_price__lt=5000)
        elif price == 'below20000':
            hoodies = hoodies.filter(discounted_price__gte=5000, discounted_price__lt=20000)
        elif price == 'below45000':
            hoodies = hoodies.filter(discounted_price__gte=20000, discounted_price__lt=45000)
        elif price == 'below70000':
            hoodies = hoodies.filter(discounted_price__gte=45000, discounted_price__lt=70000)
        elif price == 'above70000':
            hoodies = hoodies.filter(discounted_price__gte=70000)

    if query:
        hoodies = hoodies.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query)
        )

    paginator = Paginator(hoodies, 9)
    page = request.GET.get('page')
    hoodies = paginator.get_page(page)
    return render(request, 'shop/clothings/hoodie.html', {'hoodies': hoodies, 'title': 'Hoodie'})




def accessories_category_view(request, category):
    if category not in VALID_CATEGORIES:
        raise Http404("Category not found")
    
    VALID_CATEGORIES = {
    'watches': 'Watches',
    'bags': 'Bags',
    'belts': 'Belts',
    'sunglasses': 'Sunglasses',
}
    context = {
        'category': VALID_CATEGORIES[category],
    }
    return render(request, 'shop/accessories_category.html', context)

def watches_view(request):
    watches = Product.objects.filter(category__iexact='watches')
    brand = request.GET.get('brand')
    price = request.GET.get('price')
    query = request.GET.get('q')

    if brand:
        watches = watches.filter(brand__iexact=brand)

    if price:
        if price == 'below5000':
            watches = watches.filter(discounted_price__lt=5000)
        elif price == 'below20000':
            watches = watches.filter(discounted_price__gte=5000, discounted_price__lt=20000)
        elif price == 'below45000':
            watches = watches.filter(discounted_price__gte=20000, discounted_price__lt=45000)
        elif price == 'below70000':
            watches = watches.filter(discounted_price__gte=45000, discounted_price__lt=70000)
        elif price == 'above70000':
            watches = watches.filter(discounted_price__gte=70000)

    if query:
        watches = watches.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query)
        )

    paginator = Paginator(watches, 9)
    page = request.GET.get('page')
    watches = paginator.get_page(page)
    return render(request, 'shop/accessories/watch.html', {'watches': watches, 'title': 'Watches'})

def bags_view(request):
    bags = Product.objects.filter(category__iexact='bags')
    brand = request.GET.get('brand')
    price = request.GET.get('price')
    query = request.GET.get('q')

    if brand:
        bags = bags.filter(brand__iexact=brand)

    if price:
        if price == 'below5000':
            bags = bags.filter(discounted_price__lt=5000)
        elif price == 'below20000':
            bags = bags.filter(discounted_price__gte=5000, discounted_price__lt=20000)
        elif price == 'below45000':
            bags = bags.filter(discounted_price__gte=20000, discounted_price__lt=45000)
        elif price == 'below70000':
            bags = bags.filter(discounted_price__gte=45000, discounted_price__lt=70000)
        elif price == 'above70000':
            bags = bags.filter(discounted_price__gte=70000)

    if query:
        bags = bags.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query)
        )

    paginator = Paginator(bags, 9)
    page = request.GET.get('page')
    bags = paginator.get_page(page)
    return render(request, 'shop/accessories/bag.html', {'bags': bags, 'title': 'Bags'})

def belts_view(request):
    belts = Product.objects.filter(category__iexact='belts')
    brand = request.GET.get('brand')
    price = request.GET.get('price')
    query = request.GET.get('q')

    if brand:
        belts = belts.filter(brand__iexact=brand)

    if price:
        if price == 'below5000':
            belts = belts.filter(discounted_price__lt=5000)
        elif price == 'below20000':
            belts = belts.filter(discounted_price__gte=5000, discounted_price__lt=20000)
        elif price == 'below45000':
            belts = belts.filter(discounted_price__gte=20000, discounted_price__lt=45000)
        elif price == 'below70000':
            belts = belts.filter(discounted_price__gte=45000, discounted_price__lt=70000)
        elif price == 'above70000':
            belts = belts.filter(discounted_price__gte=70000)

    if query:
        belts = belts.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query)
        )

    paginator = Paginator(belts, 9)
    page = request.GET.get('page')
    belts = paginator.get_page(page)
    return render(request, 'shop/accessories/belt.html', {'belts': belts, 'title': 'Belts'})

def sunglasses_view(request):
    sunglasses = Product.objects.filter(category__iexact='sunglasses')
    brand = request.GET.get('brand')
    price = request.GET.get('price')
    query = request.GET.get('q')

    if brand:
        sunglasses = sunglasses.filter(brand__iexact=brand)

    if price:
        if price == 'below5000':
            sunglasses = sunglasses.filter(discounted_price__lt=5000)
        elif price == 'below20000':
            sunglasses = sunglasses.filter(discounted_price__gte=5000, discounted_price__lt=20000)
        elif price == 'below45000':
            sunglasses = sunglasses.filter(discounted_price__gte=20000, discounted_price__lt=45000)
        elif price == 'below70000':
            sunglasses = sunglasses.filter(discounted_price__gte=45000, discounted_price__lt=70000)
        elif price == 'above70000':
            sunglasses = sunglasses.filter(discounted_price__gte=70000)

    if query:
        sunglasses = sunglasses.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query)
        )

    paginator = Paginator(sunglasses, 9)
    page = request.GET.get('page')
    sunglasses = paginator.get_page(page)
    return render(request, 'shop/accessories/sunglass.html', {'sunglasses': sunglasses, 'title': 'Sunglasses'})



def shoes_category_view(request, category):
    if category not in VALID_SHOES_CATEGORIES:
        raise Http404("Category not found")

    VALID_SHOES_CATEGORIES = {
        'sandals': 'Sandals',
        'boots': 'Boots',
        'loafers': 'Loafers',
        'sneakers': 'Sneakers',
    }

    context = {
        'category': VALID_SHOES_CATEGORIES[category],
    }
    return render(request, 'shop/shoes_category.html', context)

def sandals_view(request):
    sandals = Product.objects.filter(category__iexact='sandals')
    brand = request.GET.get('brand')
    price = request.GET.get('price')
    query = request.GET.get('q')

    if brand:
        sandals = sandals.filter(brand__iexact=brand)

    if price:
        if price == 'below5000':
            sandals = sandals.filter(discounted_price__lt=5000)
        elif price == 'below20000':
            sandals = sandals.filter(discounted_price__gte=5000, discounted_price__lt=20000)
        elif price == 'below45000':
            sandals = sandals.filter(discounted_price__gte=20000, discounted_price__lt=45000)
        elif price == 'below70000':
            sandals = sandals.filter(discounted_price__gte=45000, discounted_price__lt=70000)
        elif price == 'above70000':
            sandals = sandals.filter(discounted_price__gte=70000)

    if query:
        sandals = sandals.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query)
        )

    paginator = Paginator(sandals, 9)
    page = request.GET.get('page')
    sandals = paginator.get_page(page)
    return render(request, 'shop/shoes/sandal.html', {'sandals': sandals, 'title': 'Sandals'})

def boots_view(request):
    boots = Product.objects.filter(category__iexact='boots')
    brand = request.GET.get('brand')
    price = request.GET.get('price')
    query = request.GET.get('q')

    if brand:
        boots = boots.filter(brand__iexact=brand)

    if price:
        if price == 'below5000':
            boots = boots.filter(discounted_price__lt=5000)
        elif price == 'below20000':
            boots = boots.filter(discounted_price__gte=5000, discounted_price__lt=20000)
        elif price == 'below45000':
            boots = boots.filter(discounted_price__gte=20000, discounted_price__lt=45000)
        elif price == 'below70000':
            boots = boots.filter(discounted_price__gte=45000, discounted_price__lt=70000)
        elif price == 'above70000':
            boots = boots.filter(discounted_price__gte=70000)

    if query:
        boots = boots.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query)
        )

    paginator = Paginator(boots, 9)
    page = request.GET.get('page')
    boots = paginator.get_page(page)
    return render(request, 'shop/shoes/boot.html', {'boots': boots, 'title': 'Boots'})

def loafers_view(request):
    loafers = Product.objects.filter(category__iexact='loafers')
    brand = request.GET.get('brand')
    price = request.GET.get('price')
    query = request.GET.get('q')

    if brand:
        loafers = loafers.filter(brand__iexact=brand)

    if price:
        if price == 'below5000':
            loafers = loafers.filter(discounted_price__lt=5000)
        elif price == 'below20000':
            loafers = loafers.filter(discounted_price__gte=5000, discounted_price__lt=20000)
        elif price == 'below45000':
            loafers = loafers.filter(discounted_price__gte=20000, discounted_price__lt=45000)
        elif price == 'below70000':
            loafers = loafers.filter(discounted_price__gte=45000, discounted_price__lt=70000)
        elif price == 'above70000':
            loafers = loafers.filter(discounted_price__gte=70000)

    if query:
        loafers = loafers.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query)
        )

    paginator = Paginator(loafers, 9)
    page = request.GET.get('page')
    loafers = paginator.get_page(page)
    return render(request, 'shop/shoes/loafers.html', {'loafers': loafers, 'title': 'Loafers'})

def sneakers_view(request):
    sneakers = Product.objects.filter(category__iexact='sneakers')
    brand = request.GET.get('brand')
    price = request.GET.get('price')
    query = request.GET.get('q')

    if brand:
        sneakers = sneakers.filter(brand__iexact=brand)

    if price:
        if price == 'below5000':
            sneakers = sneakers.filter(discounted_price__lt=5000)
        elif price == 'below20000':
            sneakers = sneakers.filter(discounted_price__gte=5000, discounted_price__lt=20000)
        elif price == 'below45000':
            sneakers = sneakers.filter(discounted_price__gte=20000, discounted_price__lt=45000)
        elif price == 'below70000':
            sneakers = sneakers.filter(discounted_price__gte=45000, discounted_price__lt=70000)
        elif price == 'above70000':
            sneakers = sneakers.filter(discounted_price__gte=70000)

    if query:
        sneakers = sneakers.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query)
        )

    paginator = Paginator(sneakers, 9)
    page = request.GET.get('page')
    sneakers = paginator.get_page(page)
    return render(request, 'shop/shoes/sneakers.html', {'sneakers': sneakers, 'title': 'Sneakers'})


class CustomerRegistrationView(View):
 def get(self, request):
   form = CustomerRegistrationForm()
   return render(request, 'shop/customerregistration.html', {'form':form})
 
 def post(self, request):
   form = CustomerRegistrationForm(request.POST)
   if form.is_valid():
     messages.success(request, 'Congratulations, registration done')
     form.save()
   return render(request, 'shop/customerregistration.html', {'form':form})
 
@login_required
def checkout(request):
 user = request.user
 add = Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=user)
 amount = 0.0
 shipping_amount = 100.0
 totalamount = 0.0
 cart_product = [p for p in Cart.objects.all() if p.user == request.user]
 if cart_product:
    for p in cart_product:
     tempamount = (p.quantity * p.product.discounted_price)
     amount += tempamount
    totalamount = amount+ shipping_amount
 return render(request, 'shop/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items})


def about(request):
    return render (request, 'shop/about.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def payment_done(request):
  user = request.user
  custid = request.GET.get('custid')
  customer = Customer.objects.get(id=custid)
  cart = Cart.objects.filter(user=user)
  for c in cart:
    OrderPlaced(user=user, customer=customer, product = c.product, quantity=c.quantity).save()
    c.delete()
  return redirect('orders')

def search(request):
    query = request.GET.get('query')
    product = Product.objects.none()  # default: empty queryset
    
    if query:
        product = Product.objects.filter(title__icontains=query)
    
    return render(request, 'shop/search.html', {'product': product})