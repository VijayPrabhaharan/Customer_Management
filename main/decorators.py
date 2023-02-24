from django.http import HttpResponse
from django.shortcuts import redirect

# functions use - if user/admin is already logged in, restricting his access to go to the login page or register page before logging out
def unauthenticated_user(view_func): 
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated: 
            return redirect('home')
        else:
            # this "view_func" changes to one of the functions in views.py while execution eg - loginpage
            return view_func(request, *args, **kwargs) 
    return wrapper_func

def allowed_users(allowed_roles=[]): # since allowed_roles parameter is required, view_func is passed in trailing function
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                # to get the first group, if user is assined in two or more groups
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)    
            else:
                return HttpResponse("You are not authorized")                 
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            # to get the first group, if user is assined in two or more groups
            group = request.user.groups.all()[0].name       
        if group == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('user')
    return wrapper_func