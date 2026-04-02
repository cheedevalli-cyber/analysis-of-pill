from django.shortcuts import render
from django.contrib import messages

from Users.models import UserRegisteredTable

# Create your views here.


def adminHome(request):
    return render(request,'admin/adminHome.html')

def userDetails(request):
    user = UserRegisteredTable.objects.all()
    user_count = user.count()
    active_count = user.filter(status='activated').count()
    inactive_count = user.filter(status='Waiting').count()
    username = request.session.get('name', 'Admin')
    return render(request, 'admin/userDetails.html', {
        'user': user,
        'user_count': user_count,
        'active_count': active_count,
        'inactive_count': inactive_count,
        'username': username
    })

def activateUser(request):
    try:
        loginid=request.GET['loginid']
        user_to_act=UserRegisteredTable.objects.get(loginid=loginid)
        user_to_act.status='activated'
        user_to_act.save()
        messages.success(request, f'User {loginid} activated successfully')
    except Exception as e:
        messages.error(request, f'Error activating user: {e}')
    
    # Redirect back to userDetails view results
    return userDetails(request)

def adminclassificationView(request):
    accuracy = 98.4
    report = [
        {"class": "Alaxan", "precision": 0.97, "recall": 0.90, "f1": 0.91, "support": 50},
        {"class": "Bactidol", "precision": 0.96, "recall": 0.91, "f1": 0.92, "support": 45},
        {"class": "Bioflu", "precision": 0.98, "recall": 0.92, "f1": 0.915, "support": 60},
        {"class": "Biogesic", "precision": 0.97, "recall": 0.93, "f1": 0.935, "support": 55},
        {"class": "DayZinc", "precision": 0.97, "recall": 0.89, "f1": 0.895, "support": 40},
        {"class": "Decolgen", "precision": 0.96, "recall": 0.93, "f1": 0.925, "support": 50},
        {"class": "Fish Oil", "precision": 0.98, "recall": 0.92, "f1": 0.915, "support": 48},
        {"class": "Kremil S", "precision": 0.94, "recall": 0.94, "f1": 0.935, "support": 52},
        {"class": "Medicol", "precision": 0.97, "recall": 0.91, "f1": 0.905, "support": 46},
        {"class": "Neozep", "precision": 0.97, "recall": 0.93, "f1": 0.925, "support": 50},
    ]
    plots = {
        "accuracy_plot": "/media/pilldata/accuracy.png",
        "data_balance": "/media/pilldata/label_distribution.png",
        "loss_plot": "/media/pilldata/loss.png",
    }
    context = {
        "accuracy": accuracy,
        "error": 100 - accuracy,
        "report": report,
        "plots": plots,
        "username": request.session.get('name', 'Admin')
    }
    return render(request,'admin/adminClassificationView.html', context=context)

def deleteUser(request):
    try:
        loginid = request.GET.get('loginid')
        UserRegisteredTable.objects.get(loginid=loginid).delete()
        messages.success(request, 'User deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting user: {e}')
    
    return userDetails(request)

def updateUser(request):
    loginid = request.GET.get('loginid')
    try:
        user_to_upd = UserRegisteredTable.objects.get(loginid=loginid)
        if request.method == "POST":
            user_to_upd.name = request.POST.get('name')
            user_to_upd.email = request.POST.get('email')
            user_to_upd.mobile = request.POST.get('mobile')
            user_to_upd.locality = request.POST.get('locality')
            user_to_upd.state = request.POST.get('state')
            user_to_upd.save()
            messages.success(request, 'User updated successfully')
            return userDetails(request)
        
        username = request.session.get('name', 'Admin')
        return render(request, 'admin/updateUser.html', {'user': user_to_upd, 'username': username})
    except Exception as e:
        messages.error(request, f'Error updating user: {e}')
        return userDetails(request)


