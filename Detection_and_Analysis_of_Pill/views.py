
from django.shortcuts import render
from django.contrib import messages
from Users.models import UserRegisteredTable

def index(request):
    return render(request,'index.html')

def loginForm(request):
    return render(request,'login.html')

def loginCheck(request):
    if request.method=="POST":
        loginid=request.POST.get('loginid')
        password=request.POST.get('password')
        
        # Check Admin Login
        if loginid=='valli' and password=='valli@2000':
            return render(request,'admin/adminHome.html')
        
        # Check User Login
        try:
            user = UserRegisteredTable.objects.get(loginid=loginid, password=password)
            if user.status == 'activated':
                return render(request,'users/userHome.html')
            else:
                messages.error(request, 'Account Status Not Activated')
                return render(request,'login.html')
        except UserRegisteredTable.DoesNotExist:
            messages.error(request, 'Invalid login credentials')
            return render(request,'login.html')
    else:
        return render(request, 'login.html')

def userRegisterForm(request):
    return render(request,'register.html')