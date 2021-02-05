from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
import random

from django.conf import settings 

from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

from .models import Category, Product,Rating
from .forms import  *
from .decorators import unauthenticated_user, allowed_users


def similar_content(u,review,A):
	list_=[]
	list_.append(str(review))
	temp=[u]
	print(len(A),A)
	for i in range(0,len(A)):
		print(A[i].customer.username)
		list_.append(str(A[i].rate))
		temp.append(str(A[i].customer.username))
	
	count = CountVectorizer()
	count_matrix = count.fit_transform(list_)
	c=cosine_similarity(count_matrix)
	d=np.sort(c[0])[::-1]
	e=np.argsort(c[0])[::-1]
	
	if (e[1]==0):
		e[1]=e[0]
	result=[]
	for i in range (1,len(d)):
		if (d[i]>=0.5):
			result.append(temp[e[i]]) 
	return result

def KMPSearch(pat, txt): 
	
	M = len(pat) 
	N = len(txt) 

	lps = [None] * M 
	j = 0 # index for pat[] 

	computeLPSArray(pat, M, lps) 

	i = 0 # index for txt[] 
	res = 0
	next_i = 0

	while (i < N): 
		if pat[j] == txt[i]: 
			j = j + 1
			i = i + 1
		if j == M: 
			
			j = lps[j - 1] 
			res = res + 1

			if lps[j] != 0: 
				next_i = next_i + 1
				i = next_i 
				j = 0

		elif ((i < N) and (pat[j] != txt[i])): 
			
			if (j != 0): 
				j = lps[j - 1] 
			else: 
				i = i + 1
				
	return res 
def computeLPSArray(pat, M, lps): 
	
	len = 0
	i = 1
	lps[0] = 0 # lps[0] is always 0 

	while (i < M): 
		if pat[i] == pat[len]: 
			len = len + 1
			lps[i] = len
			i = i + 1
			
		else: # (pat[i] != pat[len]) 
		
			if len != 0: 
				len = lps[len - 1] 
				
			else: # if (len == 0) 
				lps[i] = len
				i = i + 1

def cheak_username(arr):
	H=Product.objects.all()
	h=Product.objects.count()
	a=["sennheiser","jbl","sony","boat","mi","samsung","realme","jockey","tata","raymonds","hp","dell","mavic","drone","woodland"
		,"redchief","pepsodent","modi","iit","cocacola","puma","flipkart","starbuks","kfc","cobra","gucci","channel","anglepriya","somanbefawaha","tomyhighflyer"]	
	    
	k=arr.lower()
	for j in range(0,h):
		a.append(H[j].name)
	for i in a:
		if i in k:
		    return 1;
	
	return 0;
def check1(review):
	H=Product.objects.all()
	h=Product.objects.count()
	a=["sennheiser","jbl","sony","boat","mi","samsung","realme","jockey","tata","raymonds","hp","dell","mavic","drone","woodland"
		,"redchief","pepsodent","modi","iit","cocacola","puma","flipkart","starbuks","kfc","cobra","gucci","channel","anglepriya","somanbefawaha","tomyhighflyer"]	
	for j in range(0,h):
		a.append(H[j].name)
		print(type(H[j].name))
   
	k=review.lower()
	for i in a:
		a=KMPSearch(i, review)
		if(a>4):
		    return 1;
	return 0;

def check(u,A):
	
        for i in range(0,len(A)):

                if u==str(A[i].customer.username):
                        return 1


        return 0
                        

OTP=random.randint(1000,9999)

glo=''
@unauthenticated_user
def registerPage(request):

	
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		global glo
		glo=form
		if form.is_valid():
			
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			if cheak_username(username):
				messages.info(request, 'your username should not containt a product name or brand name')
				
				return redirect('spm_ck:register')
			count=User.objects.count()
			Q=User.objects.all()
			for i in range(count):
				q=Q[i].email
				if q==email:
					messages.info(request, 'Account is Already created')
					print('error')
					return redirect('spm_ck:register')
			else:
				messages.success(request, 'Account was created for ' + username)
			        
				subject = 'Email Verfication'
				message = f'Hi {username}, This is your OTP for Verification. '  + str(OTP)       
				email_from = settings.EMAIL_HOST_USER 
				recipient_list = [email, ] 
				send_mail( subject, message, email_from, recipient_list ) 
				return render(request, 'spm_ck/verify.html')

       
	form = CreateUserForm()
	context = {'form':form}


	return render(request, 'spm_ck/users/register.html', context)

def velidate(request):
	if request.method == 'POST':
		otp = request.POST.get('otp')
		if int(otp)==OTP:
			user = glo.save()
			return redirect('spm_ck:login') 
			
                      
		return render(request, 'spm_ck/verify.html')
   

     


@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('spm_ck:product_list')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'spm_ck/users/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('spm_ck:login')

@login_required(login_url='spm_ck:login')
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'spm_ck/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

@login_required(login_url='spm_ck:login')
def product_detail(request, id, slug):
	B=Product.objects.get(pk=id)
    
	A = Rating.objects.filter(rated_product=B)

	product = get_object_or_404(Product,
		                id=id,
		                slug=slug,
		                available=True)
	return render(request,
		  'spm_ck/product/detail.html',
		  {'product': product,'A': A})

@login_required(login_url='spm_ck:login')
def createOrder(request,id):
	B=Product.objects.get(pk=id)
	form = OrderForm(initial={'customer':request.user,'rated_product':B})
	form.fields['rated_product'].widget = forms.HiddenInput()
	form.fields['customer'].widget = forms.HiddenInput()
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			S = Rating.objects.all()
			print(request.user.username)
			result = similar_content(str(request.user.username),str(request.POST.get('rate')),S)
			print(result)
			SS = Rating.objects.filter(rated_product=B)
			if len(result) !=0 :
				file = open('test.txt','a')
				file.write(str(request.user.username)+" (content similar) with : \n")
				for i in result:
					file.write(i+"\n")
				file.close()         
			elif(cheak_username(str(request.user.username))):
				file = open('test.txt','a')
				file.write(str(request.user.username)+" (user name contain a product name) \n")
				file.close()       
			elif(check(str(request.user.username),SS)):
                                file = open('test.txt','a')
                                file.write(str(request.user.username)+" (multiple reviews on same product) \n")
                                file.close()
			elif(check1(str(request.POST.get('rate')))):
				file = open('test.txt','a')
				file.write(str(request.user.username)+" (user's review contain product name more than 4 times) \n")
				file.close()
			else:
				form.save()
			return redirect('/')
	context = {'form':form}
	return render(request, 'spm_ck/order_form.html', context)


