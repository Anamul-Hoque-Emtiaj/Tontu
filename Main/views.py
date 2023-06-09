from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from .models import Banner,Category,Product,ProductAttribute,CartOrder,CartOrderItems,ProductReview,Wishlist,UserAddressBook
from django.contrib.auth.models import User
from django.db.models import Max,Min,Count,Avg
from django.db.models.functions import ExtractMonth
from django.template.loader import render_to_string
from .forms import SignupForm,ReviewAdd,AddressBookForm,ProfileForm 
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required

# Home Page
def home(request):
	banners=Banner.objects.all().order_by('-id')
	data=Product.objects.order_by('-id')
	cats=Category.objects.all().order_by('-id')
	return render(request,'index.html',{'data':data,'banners':banners,'cats':cats})

def test(request):
	banners=Banner.objects.all().order_by('-id')
	data=Product.objects.order_by('-id')
	cats=Category.objects.all().order_by('-id')
	return render(request,'base_core.html',{'data':data,'banners':banners,'cats':cats})

def error_404(request, exception):
	return render(request,'error.html',{'msg':'page_not_found','code':404})
    

# def error_500(request,  exception):
#     return render(request,'error.html',{'msg':'internal_server_error','code':500})
        
def error_403(request, exception):

    return render(request,'error.html',{'msg':'forbidden_error','code':403})

def error_400(request,  exception):
    return render(request,'error.html',{'msg':'bad_request_error','code':400}) 

# Category
def category_list(request):
    data=Category.objects.all().order_by('-id')
    return render(request,'category_list.html',{'data':data})


# Product List
def product_list(request):
	total_data=Product.objects.count()
	data=Product.objects.all().order_by('-id')
	min_price=ProductAttribute.objects.aggregate(Min('price'))
	max_price=ProductAttribute.objects.aggregate(Max('price'))
	return render(request,'product_list.html',
		{
			'data':data,
			'total_data':total_data,
			'min_price':min_price,
			'max_price':max_price,
		}
		)

# Product List According to Category
def category_product_list(request,cat_id):
	category=Category.objects.get(id=cat_id)
	total_data=Product.objects.filter(category=category).count()
	data=Product.objects.filter(category=category).order_by('-id')
	min_price=ProductAttribute.objects.aggregate(Min('price'))
	max_price=ProductAttribute.objects.aggregate(Max('price'))
	return render(request,'category_product_list.html',{
			'data':data,
			'total_data':total_data,
			'category':category,
			'min_price':min_price,
			'max_price':max_price
			})


# Product Detail
def product_detail(request,slug,id):
	product=Product.objects.get(id=id)
	related_products=Product.objects.filter(category=product.category).exclude(id=id)[:4]
	colors=ProductAttribute.objects.filter(product=product).values('color__id','color__title','color__color_code').distinct()
	reviewForm=ReviewAdd()

	print(id,slug)
	# Check
	canAdd=True
	reviewCheck=ProductReview.objects.filter(product=product).count()
	if request.user.is_authenticated:
		if reviewCheck > 0:
			canAdd=False
	# End

	# Fetch reviews
	reviews=ProductReview.objects.filter(product=product)
	# End

	# Fetch avg rating for reviews
	avg_reviews=ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
	# End

	return render(request, 'product_detail.html',{'data':product,'related':related_products,'colors':colors,'reviewForm':reviewForm,'canAdd':canAdd,'reviews':reviews,'avg_reviews':avg_reviews})

# Search
def search(request):
	q=request.GET['q']
	data=Product.objects.filter(title__icontains=q).order_by('-id')
	return render(request,'search.html',{'data':data})

# Filter Data
def filter_data(request):
	colors=request.GET.getlist('color[]')
	categories=request.GET.getlist('category[]')
	minPrice=request.GET['minPrice']
	maxPrice=request.GET['maxPrice']
	allProducts=Product.objects.all().order_by('-id').distinct()
	allProducts=allProducts.filter(productattribute__price__gte=minPrice)
	allProducts=allProducts.filter(productattribute__price__lte=maxPrice)
	if len(colors)>0:
		allProducts=allProducts.filter(productattribute__color__id__in=colors).distinct()
	if len(categories)>0:
		allProducts=allProducts.filter(category__id__in=categories).distinct()
	
	t=render_to_string('ajax/product-list.html',{'data':allProducts,'user':request.user})
	return JsonResponse({'data':t})

# Load More
def load_more_data(request):
	offset=int(request.GET['offset'])
	limit=int(request.GET['limit'])
	data=Product.objects.all().order_by('-id')[offset:offset+limit]
	t=render_to_string('ajax/product-list.html',{'data':data,'user':request.user})
	return JsonResponse({'data':t})

# Add to cart
@login_required
def add_to_cart(request):
	if not request.user.is_authenticated:
		return redirect('/accounts/login/')
	# del request.session['cartdata']
	cart_p={}
	cart_p[str(request.GET['id'])]={
		'image':request.GET['image'],
		'title':request.GET['title'],
		'qty':request.GET['qty'],
		'price':request.GET['price'],
	}
	print(cart_p)
	if 'cartdata' in request.session:
		if str(request.GET['id']) in request.session['cartdata']:
			cart_data=request.session['cartdata']
			cart_data[str(request.GET['id'])]['qty']=int(cart_p[str(request.GET['id'])]['qty'])
			cart_data.update(cart_data)
			request.session['cartdata']=cart_data
		else:
			cart_data=request.session['cartdata']
			cart_data.update(cart_p)
			request.session['cartdata']=cart_data
	else:
		request.session['cartdata']=cart_p
	return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})

# Cart List Page
@login_required
def cart_list(request):
	total_amt=0
	if 'cartdata' in request.session:
		for p_id,item in request.session['cartdata'].items():
			print(item['qty'],item['price'])
			total_amt+=int(item['qty'])*int(item['price'])
		return render(request, 'cart.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	else:
		return render(request, 'cart.html',{'cart_data':'','totalitems':0,'total_amt':total_amt})


# Delete Cart Item
@login_required
def delete_cart_item(request):
	p_id=str(request.GET['id'])
	if 'cartdata' in request.session:
		if p_id in request.session['cartdata']:
			cart_data=request.session['cartdata']
			del request.session['cartdata'][p_id]
			request.session['cartdata']=cart_data
	total_amt=0
	for p_id,item in request.session['cartdata'].items():
		total_amt+=int(item['qty'])*float(item['price'])
	t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

# Delete Cart Item
@login_required
def update_cart_item(request):
	p_id=str(request.GET['id'])
	p_qty=request.GET['qty']
	if 'cartdata' in request.session:
		if p_id in request.session['cartdata']:
			cart_data=request.session['cartdata']
			cart_data[str(request.GET['id'])]['qty']=p_qty
			request.session['cartdata']=cart_data
	total_amt=0
	for p_id,item in request.session['cartdata'].items():
		total_amt+=int(item['qty'])*float(item['price'])
	t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

# Signup Form
def signup(request):
	if request.method=='POST':
		user = request.POST
		if user['password1'] != user['password2']:
			return render(request, 'registration/signup.html',{'error':'password didnot matched'})
		if User.objects.filter(username = user['username']):
			return render(request, 'registration/signup.html',{'error':'UserName already exist'})
		if User.objects.filter(email = len(user['password1'])<8):
			return render(request, 'registration/signup.html',{'error':'Password length Must be greater than 8'})
        	
		user1 = User.objects.create_user(
			first_name = user['first_name'],
			last_name = user['last_name'],
			email = user['email'],
			username= user['username'],
			password= user['password1']
		)
		user2=authenticate(username=user['username'],password=user['password1'])
		login(request, user2)
		return redirect('home')
	return render(request, 'registration/signup.html')
#login
def login(request):
	if request.method == 'POST':
		if not User.objects.filter(username = request.POST['username']):
			return render(request, 'registration/login.html',{'error':'Username not found'})
		user = User.objects.filter(username = request.POST['username'])
		if not user.check_password(request.POST['password']):
			return render(request, 'registration/login.html',{'error':'Password did not match'})
		user2=authenticate(username=request.POST['username'],password=request.POST['password'])
		login(request, user2)
		return redirect('home')

	return render(request, 'registration/login.html')

#password_change 
@login_required
def password_change(request):
	msg=None
	if request.method=='POST':
		user = request.POST
		user1=User.objects.get(username = request.user)
		print(user)
		if not user1.check_password(user['password3']):
			msg = 'Old Password did not match'
		elif user['password1'] != user['password2']:
			msg = 'Passwords did not match'
		else:
			msg='Password changed'
			user1.set_password(user['password1'])
			user1.save()
	return render(request, 'user/password_change.html',{'error':msg})

# Checkout
@login_required
def checkout(request):
	totalAmt=0
	for p_id,item in request.session['cartdata'].items():
		totalAmt+=float(item['qty'])*float(item['price'])
	address=UserAddressBook.objects.filter(user=request.user).first()
	if request.method=='POST':
		if 'cartdata' in request.session:
			if(UserAddressBook.objects.filter(user = request.user,mobile= request.POST["mobile"],city = request.POST["city"],street_address  = request.POST["street_address"])):
				address2 = address
			else:
				address2 = UserAddressBook.objects.create(
				user = request.user,
				mobile= request.POST["mobile"],
				country= request.POST["country"],
				city = request.POST["city"],
				street_address  = request.POST["street_address"],
				zipcode = request.POST["zipcode"]
			)
			order=CartOrder.objects.create(
					user=request.user,
					billing_address = address2,
					total_amt=totalAmt
				)
			# End
			for p_id,item in request.session['cartdata'].items():
				# OrderItems
				items=CartOrderItems.objects.create(
					order=order,
					invoice_no='INV-'+str(order.id),
					item=item['title'],
					image=item['image'],
					qty=item['qty'],
					price=item['price'],
					total=float(item['qty'])*float(item['price'])
					)
				# End
			
			
			del request.session['cartdata']
			return redirect('/my-orders')
	
	if 'cartdata' in request.session:
		return render(request, 'checkout.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':totalAmt,'address':address})
	else:
		return redirect('/')



# Save Review
@login_required
def save_review(request,pid):
	product=Product.objects.get(pk=pid)
	user=request.user
	review=ProductReview.objects.create(
		user=user,
		product=product,
		review_text=request.POST['review_text'],
		review_rating=request.POST['review_rating'],
		)
	cnt = product.review
	
	avg_reviews=ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
	product.rating = avg_reviews['avg_rating']
	product.review = cnt+1
	product.save()
	data={
		'user':user.username,
		'review_text':request.POST['review_text'],
		'review_rating':request.POST['review_rating']
	}


	return JsonResponse({'bool':True,'data':data,'avg_reviews':avg_reviews})

# User Dashboard
import calendar
@login_required
def my_dashboard(request):
	orders=CartOrder.objects.annotate(month=ExtractMonth('order_dt')).values('month').annotate(count=Count('id')).values('month','count').filter(user=request.user)
	monthNumber=[]
	totalOrders=[]
	for d in orders:
		monthNumber.append(calendar.month_name[d['month']])
		totalOrders.append(d['count'])
	return render(request, 'user/dashboard.html',{'monthNumber':monthNumber,'totalOrders':totalOrders})

# My Orders
@login_required
def my_orders(request):
	orders=CartOrder.objects.filter(user=request.user).order_by('-id')
	return render(request, 'user/orders.html',{'orders':orders,'totalitems':len(orders)})

# Order Detail
@login_required
def my_order_items(request,id):
	order=CartOrder.objects.get(pk=id)
	orderitems=CartOrderItems.objects.filter(order=order).order_by('-id')
	return render(request, 'user/order-items.html',{'orderitems':orderitems,'id':id, 'order':order})

# Wishlist
@login_required
def add_wishlist(request):
	pid=request.GET['product']
	product=Product.objects.get(pk=pid)
	data={}
	checkw=Wishlist.objects.filter(product=product,user=request.user).count()
	if checkw > 0:
		data={
			'bool':False
		}
	else:
		wishlist=Wishlist.objects.create(
			product=product,
			user=request.user
		)
		data={
			'bool':True
		}
	return JsonResponse(data)

# My Wishlist
@login_required
def my_wishlist(request):
	wlist=Wishlist.objects.filter(user=request.user).order_by('-id')
	return render(request, 'wishlist.html',{'wlist':wlist,'totalitems':len(wlist)})
@login_required
def delete_from_wishlist(request,id):
	product = Product.objects.get(pk=id)
	Wishlist.objects.filter(product=product,user=request.user).delete()
	wlist=Wishlist.objects.filter(user=request.user).order_by('-id')
	return render(request, 'wishlist.html',{'wlist':wlist,'totalitems':len(wlist)})
# My Reviews
@login_required
def my_reviews(request):
	reviews=ProductReview.objects.filter(user=request.user).order_by('-id')
	return render(request, 'user/reviews.html',{'reviews':reviews,'totalitems':len(reviews)})

# Edit Profile
@login_required
def edit_profile(request):
	msg=None
	if request.method=='POST':
		user = request.POST
		user1=User.objects.get(username = request.user)
		print(user)
		if not user1.check_password(user['password']):
			msg = 'Password did not match'
		else:
			msg='Data has been saved'
			user1.first_name = user['first_name']
			user1.last_name = user['last_name']
			user1.email = user['email']
			user1.save()
	return render(request, 'user/edit-profile.html',{'error':msg})

def password(request):
	return redirect('/accounts/password_change/')

def about_us(request):
	return render(request, 'about.html')