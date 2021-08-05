from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from rango.models import Category, Product
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm, ProductForm
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
        prodcut = Product.objects.get(slug=product_name_slug)

        # products = Product.objects.filter(category=category)

        # context_dict['products'] = products
        context_dict['product'] = prodcut
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



@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    # You cannot add a page to a Category that does not exist...
    if category is None:
        return redirect(reverse('rango:index'))

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

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
    context_dict = {'user': request.user}
    return render(request, 'rango/buyer_my_account.html', context=context_dict)

@login_required
def collections(request):
        return render(request, 'rango/collections.html')

@login_required
def cart(request):
        return render(request, 'rango/cart.html')

@login_required
def order_history(request):
        return render(request, 'rango/order_history.html')

@login_required
def payment(request):
    context_dict = {'user': request.user}
    return render(request, 'rango/payment.html', context=context_dict)

@login_required
def seller_my_account(request):
        return render(request, 'rango/seller_my_account.html')



def remove_product (request):
        return render(request, 'rango/remove_product.html')

def products_and_sales (request):
        return render(request, 'rango/products_and_sales.html')

def product_search (request):
        return render(request, 'rango/product_search.html')















