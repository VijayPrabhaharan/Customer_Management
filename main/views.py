from tokenize import group
from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseNotFound

from .models import *

from .form import *

from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

# to restrict access to view the pages when the user/admin is not logged in 
from django.contrib.auth.decorators import login_required

from .decorators import *

from django.contrib.auth.models import  Group
# Create your views here.

@unauthenticated_user # from "decorators.py"
def loginpage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username or Password is incorrect')
	return render(request, 'login.html')

@unauthenticated_user # from "decorators.py"
def registerpage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			group = Group.objects.get(name='customer(or)user')
			# to group all the newly signed up user to the customer(or)user group
			user.groups.add(group)   
			# to create one to one relationship                          
			Customer.objects.create(user=user,)				
			messages.success(request, 'Account has been created for ' + username + '!')
			return redirect('login')
	return render(request, 'register.html', {'form': form})

def logoutpage(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@admin_only # from decorators.py
def home(request):
	customers = Customer.objects.all()
	orders = Order.objects.all().order_by('-date_created')
	total_customers = customers.count()
	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	shipped = orders.filter(status='Shipped').count()
	return render(request, 'dashboard.html', {'customers': customers, 'orders': orders, 'total_orders': total_orders, 'delivered': delivered, 'pending': pending, 'shipped': shipped})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
	products = Product.objects.all()
	return render(request, 'products.html', {'products': products})


@login_required(login_url='login')
def customer(request, pk):
	customer = Customer.objects.get(id=pk)
	orders = customer.order_set.all()
	orders_count = orders.count()
	return render(request, 'customer.html', {'customer': customer, 'orders': orders, 'orders_count': orders_count})

@login_required(login_url='login')
def createOrder(request):
	form = OrderForm()
	if request.method=="POST":
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	return render(request, 'order_form.html', {'form': form})

@login_required(login_url='login')
def updateOrder(request, pk):
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)
	if request.method=="POST":
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')
	return render(request, 'order_form.html', {'form': form})

@login_required(login_url='login')
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method=="POST":
		order.delete()
		return redirect('/')
	return render(request, 'delete_order.html')

@login_required(login_url='login')
def createCustomer(request):
	form = CustomerForm()
	if request.method=="POST":
		form = CustomerForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	return render(request, 'create_customer.html', {'form': form})

@login_required(login_url='login')
def updateCustomer(request, pk):
	customer = Customer.objects.get(id=pk)
	form = CustomerForm(instance=customer)
	if request.method=="POST":
		form = CustomerForm(request.POST, instance=customer)
		if form.is_valid():
			form.save()
			return redirect('/')
	return render(request, 'create_customer.html', {'form': form})

@login_required(login_url='login')
def deleteCustomer(request, pk):
	customer = Customer.objects.get(id=pk)
	if request.method=="POST":
		customer.delete()
		return redirect('/')
	return render(request, 'delete_customer.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer(or)user'])
def userpage(request):
	# since user column is created in customer table, 
	# customer is an attribute of user
	orders = request.user.customer.order_set.all() 										  
	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	shipped = orders.filter(status='Shipped').count()
	context = {'orders': orders, 'total_orders': total_orders, 'delivered': delivered, 'pending': pending, 'shipped': shipped}
	return render(request, 'user.html', context)


@login_required(login_url='login')
# for settings page
def account_settings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)
	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES, instance=customer)
		if form.is_valid():
			form.save()
	context = {'form':form}
	return render(request, 'account_settings.html', context)



