from django.shortcuts import redirect

def require_anon(func):
    def decorator(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return func(request, *args, **kwargs)

    return decorator