from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated: 
            if request.user.is_freelancer:
                return redirect('browseProject') # home page
            elif request.user.is_client:
                return redirect('clientProject')
        
        return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            if request.user.is_freelancer and 'freelancer' in allowed_roles:
                return view_func(request, *args, **kwargs)
            elif request.user.is_client and 'client' in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not God to view this page bro')
        return wrapper_func
    return decorator
