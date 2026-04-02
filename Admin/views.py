from django.shortcuts import render
from django.contrib import messages

from Users.models import UserRegisteredTable

# Create your views here.


def adminHome(request):
    return render(request,'admin/adminHome.html')

def userDetails(request):
    user=UserRegisteredTable.objects.all()
    return render(request,'admin/userDetails.html',{'user':user})

def activateUser(request):
    loginid=request.GET['loginid']
    user=UserRegisteredTable.objects.get(loginid=loginid)
    user.status='activated'
    user.save()
    userr=UserRegisteredTable.objects.all()
    return render(request,'admin/userDetails.html',{'user':userr})

def adminclassificationView(request):
    from Users.utility.requirement import main
    accuracy,precision,recall=main()
    return render(request,'users/classificationView.html',context={'accurecy':accuracy,'precision':precision,'recall':recall})


