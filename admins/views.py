from django.contrib import messages
from django.shortcuts import render, redirect
from users.models import UserRegistrationModel, UserActivityLog, PredictionReport


# Create your views here.
def AdminLoginCheck(request):
    if request.method == 'POST':
        usrid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("User ID is = ", usrid)
        if usrid == 'admin' and pswd == 'admin':
            log = UserActivityLog.objects.create(user_loginid='admin', user_role='Admin')
            request.session['log_id'] = log.id
            return render(request, 'admins/AdminHome.html')
        else:
            messages.success(request, 'Please Check Your Login Details')
    return render(request, 'AdminLogin.html', {})


def AdminHome(request):
    return render(request, 'admins/AdminHome.html')


def RegisterUsersView(request):
    data = UserRegistrationModel.objects.all()
    return render(request, 'admins/viewregisterusers.html', {'data': data})


def ActivaUsers(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        status = 'activated'
        print("PID = ", id, status)
        UserRegistrationModel.objects.filter(id=id).update(status=status)
        return redirect('RegisterUsersView')

def DeleteUser(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        UserRegistrationModel.objects.filter(id=id).delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('RegisterUsersView')

def EditUser(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        user = UserRegistrationModel.objects.get(id=id)
        return render(request, 'admins/edituser.html', {'user': user})
    elif request.method == 'POST':
        id = request.POST.get('uid')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        locality = request.POST.get('locality')
        status = request.POST.get('status')
        role = request.POST.get('role')
        UserRegistrationModel.objects.filter(id=id).update(name=name, mobile=mobile, email=email, locality=locality, status=status, role=role)
        messages.success(request, 'User updated successfully.')
        return redirect('RegisterUsersView')

def ViewActivityLog(request):
    data = UserActivityLog.objects.all().order_by('-login_time')
    return render(request, 'admins/ActivityLog.html', {'data': data})

def ViewPredictionReport(request):
    data = PredictionReport.objects.all().order_by('-created_at')
    return render(request, 'admins/PredictionReport.html', {'data': data})