from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
#from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.template import RequestContext
from inventory.forms import IssueProductForm, ReceiveProductForm, ProductForm, CategoryForm, EditProductDetails
from inventory.models import Category, Product, IssueProduct, ReceiveProduct
from django.db import transaction

'''from inventory.models import Product, Category, CategoryForm, ProductForm, ReceiveProduct, ReceiveProductForm
from inventory.models import IssueProduct, IssueProductForm'''



# Create views here

def home(request):
    return render_to_response('inventory/home.html')


def mylogin(request):
    c_users = {} # set c to empty dictionary
    c_users.update(csrf(request))
    #username = password = ''
    return render_to_response('inventory/login.html', c_users) #context_instance=RequestContext(request))
    #return render_to_response('inventory/login.html', username)


def auth_view(request):
    username = request.POST.get('username', '') # add empty string if field is empty
    password = request.POST.get('password', '')
    user = authenticate(username=username,
                        password=password) #auth.authenticate() used to validate user before passing to logged in page

    if user is not None:
        if user.is_active:
            login(request, user) #set user as logged in using the login method
            #return render_to_response('inventory/loggedin.html')
            return HttpResponseRedirect('loggedin')
        else:
            return HttpResponseRedirect('inactive')
    else:
        #return render_to_response('inventory/invalid.html')
         return HttpResponseRedirect('invalid')


def loggedin(request):
    return render_to_response('inventory/loggedin.html',
                              {'logged_user': request.user.username}) # request.user properties


def invalid_login(request):
    return render_to_response('inventory/invalid.html')


def mylogout(request):
    logout(request)
    return render_to_response('inventory/logout.html')

@login_required()
def addproduct(request):

    # list all the categories of products

    all_categories = Category.objects.all()
    #categories = {'categories': all_categories}

    # create new instance of product
    message = ""
    if request.method == 'POST':
        #_product = Product()
        form = ProductForm(request.POST)#, instance=_product)
        if form.is_valid():
            form.save()
            new_product = form.cleaned_data['name']

            # print message on successful save of product
            message = "%s product successfully added" % new_product
            # Clear form after submission
            form = ProductForm()

    else:
        form = ProductForm()

    # create empty dictionary for when page is first visited and no form posted
    context = {}
    context.update(csrf(request))

    # Add message and all_categories to product dict
    context['message'] = message
    context['all_categories'] = all_categories
    context['form'] = form

    return render_to_response('inventory/addproduct.html', context)

@login_required()
def addcategory(request):

    # Create new instance of Category object
    message = ""
    if request.method == 'POST':
        _category = Category()
        _category = CategoryForm(request.POST, instance=_category)
        new_category = _category.save()
        message = "%s category successfully added" % new_category
        #return HttpResponse(message)

        #add functionality to print successful message after save



    #Cater for when no post has been made from the form
    args = {} #set args to an empty dictionary
    args.update(csrf(request))
    args['message'] = message

    return render_to_response('inventory/addcategory.html', args)

@login_required()
def receiveproduct(request):

    message = ""
    if request.method == 'POST':
        form = ReceiveProductForm(request.POST)
        if form.is_valid():
            prod = form.save()
            received_item_name = form.cleaned_data['name']
            received_item_qty = form.cleaned_data['quantity']
            #item_id = form.cleaned_data['name'].id
            #item_id = prod.id

            # Display product balance after items received
            received_product = prod.name
            received_item_total = received_product.current_quantity()
            received_item_total_value = received_product.current_quantity_value()

            message = "%s %s item(s) successfully received and current total is %s, and value is %s" % (received_item_qty, received_item_name, received_item_total, received_item_total_value)

            # Clear form after submission
            form = ReceiveProductForm()

    else:
        form = ReceiveProductForm()

    context = {}
    context.update(csrf(request))
    context['message'] = message
    context['form'] = form

    return render_to_response('inventory/receiveproduct.html', context)

@login_required()
@transaction.commit_manually # add manual transaction commit to rollback negative values to DB
def issueproduct(request):

    message = ""
    if request.method == 'POST':
        form = IssueProductForm(request.POST)
        if form.is_valid():
            # do not commit changes to DB until check for negative value is completed
            #prod = form.save(commit=False)
            prod = form.save()
            issued_item_qty = form.cleaned_data['quantity']
            issued_item_name = form.cleaned_data['name']
            #import pdb; pdb.set_trace()

            # display the balance of products after items have been issued
            issued_product = prod.name
            issued_item_total = issued_product.current_quantity()

            issued_item_total_value = issued_product.current_quantity_value()

            if issued_item_total_value < 0:
                # rollback transaction if value is negative
                transaction.rollback()
                message = "You cannot issue a quantity more than that received"

            else:
                # commit transaction if value is positive
                #transaction.commit()
                message = "%s %s item(s) successfully issued and the current total is %s, and value is %s" % (issued_item_qty,issued_item_name, issued_item_total, issued_item_total_value)

            # Clear form after submission
            form = IssueProductForm()
    else:
        form = IssueProductForm()

    context = {}
    context.update(csrf(request))
    context['message'] = message
    context['form'] = form

    # fix for form commit/rollback error message
    return_value = render_to_response('inventory/issueproduct.html', context)
    transaction.commit()
    return return_value

    #return render_to_response('inventory/issueproduct.html', context)


def inactive(request):
    return render_to_response('inventory/inactive.html')


def view_product(request):
    """
    This page allows the user to select a product and view the product name, price, quantity and total price value
    """

    # select a product from the products drop down list
    message = ""
    if request.method == 'POST':
        form = EditProductDetails(request.POST)

        if form.is_valid():
            prod = form.save()
            prod_name = form.cleaned_data['name']
            prod_price = form.cleaned_data['price']
            #prod_name = prod.name
            #prod_price = prod.price
            selected_product = prod.name
            prod_total_value = selected_product.current_quantity_value()
            message = "The %s product(s) has a unit price and value of %s" % (prod_name, prod_total_value)

    else:
        form = EditProductDetails()

    context = {}
    context.update(csrf(request))
    context['form'] = form
    context['message'] = message
    # context['prod_name'] = prod_name
    # context['prod_price'] = prod_price
    # context['prod_total_value']= prod_total_value

    return render_to_response('inventory/view_product.html', context)


# Define view for admin site

def admin_site(request):
    HttpResponseRedirect('admin')