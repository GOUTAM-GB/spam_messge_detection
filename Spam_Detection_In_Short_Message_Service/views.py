from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from users.forms import UserRegistrationForm
from users.models import UserRegistrationModel, UserActivityLog

def index(request):
    return render(request, 'index.html', {})

def logout(request):
    log_id = request.session.get('log_id')
    if log_id:
        UserActivityLog.objects.filter(id=log_id).update(logout_time=timezone.now())
    request.session.flush()
    return redirect('index')

def UnifiedLogin(request):
    return render(request, 'UserLogin.html', {})

def UserRegister(request):
    form = UserRegistrationForm()
    return render(request, 'UserRegistrations.html', {'form': form})

def LoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        
        # Hardcoded super admin fallback
        if loginid == 'admin' and pswd == 'admin':
            log = UserActivityLog.objects.create(user_loginid='admin', user_role='Admin')
            request.session['log_id'] = log.id
            return render(request, 'admins/AdminHome.html', {})
            
        # Check database for registered users/admins
        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            if check.status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                log = UserActivityLog.objects.create(user_loginid=loginid, user_role=check.role)
                request.session['log_id'] = log.id
                
                if check.role.lower() == 'admin':
                    return render(request, 'admins/AdminHome.html', {})
                else:
                    return render(request, 'users/UserHomePage.html', {})
            else:
                messages.success(request, 'Your Account is not activated')
                return render(request, 'UserLogin.html', {})
        except Exception as e:
            import traceback
            print("LOGIN FAILED EXCEPTION:")
            traceback.print_exc()
            messages.success(request, f'Login failed due to system error: {str(e)}')
            return render(request, 'UserLogin.html', {})
            
    return render(request, 'UserLogin.html', {})