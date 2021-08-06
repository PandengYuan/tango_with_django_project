from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from rango.models import Category, Product, Cart
from rango.forms import CategoryForm, UserForm, UserProfileForm, ProductForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime


def index(request):
    category_list = Category.objects.order_by('-sales')[:5]
    product_list = Product.objects.order_by('-sales')[:5]

    context_dict = {}
    context_dict['categories'] = category_list
    context_dict['products'] = product_list

    visitor_cookie_handler(request)
    # context_dict['visits'] = request.session['visits']
    response = render(request, 'rango/index.html', context=context_dict)
    return response


def show_category(request, category_name_slug):

    context_dict = {}

    category_list = Category.objects

    try:
        category = Category.objects.get(slug=category_name_slug)

        products = Product.objects.filter(category=category)

        context_dict['products'] = products
        context_dict['category'] = category
        context_dict['categories'] = category_list
    except Category.DoesNotExist:

        context_dict['category'] = None
        context_dict['products'] = None
        context_dict['categories'] = None

    return render(request, 'rango/category.html', context=context_dict)



def show_product(request, product_name_slug):

    context_dict = {}

    product_list = Product.objects

    try:
        product = Product.objects.get(slug=product_name_slug)

        # products = Product.objects.filter(category=category)

        # context_dict['products'] = products
        context_dict['product'] = product
        # context_dict['products'] = category_list
    except Category.DoesNotExist:

        context_dict['product'] = None
        # context_dict['produucts'] = None
        # context_dict['categories'] = None

    return render(request, 'rango/product.html', context=context_dict)


@login_required
def add_category(request):

    form = CategoryForm()
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():

            form.save(commit=True)

            return redirect(reverse('rango:index'))
        else:

            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})



@login_required
def upload_product(request):
   
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():

            product = form.save(commit=True)
            product.save()

            return redirect(reverse('rango:seller_my_account'))
        else:
            print(form.errors)

    context_dict = {'form': form}
    return render(request, 'rango/upload_product.html', {'form': form})


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 'rango/register.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html')


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    
    request.session['visits'] = visits


@login_required
def buyer_my_account(request):
    return render(request, 'rango/buyer_my_account.html')


@login_required
def seller_my_account(request):
    return render(request, 'rango/seller_my_account.html')


@login_required
def cart(request):
    products = Product.objects.all()
    carts = Cart.objects.all()
    username = request.user.username
    product_list = []
    for item in carts:
        if item.buyer_name == username:
            for p in products:
                if item.product_name == p.name:
                    product_list.append(p)

    context_dict = {'products': product_list}
    return render(request, 'rango/cart.html',context=context_dict)


@login_required
def payment(request):
    context_dict = {'user': request.user}
    return render(request, 'rango/payment.html', context=context_dict)


@login_required
def remove_product (request):
    context_dict = {}
    context_dict['products'] = Product.objects.all()
    return render(request, 'rango/remove_product.html',context=context_dict)


def product_search (request):
    context_dict = {}
    context_dict['products'] = Product.objects.all()
    context_dict['categories'] = Category.objects.all()
    return render(request, 'rango/product_search.html', context=context_dict)















