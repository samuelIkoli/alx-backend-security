from django.http import JsonResponse
from ratelimit.decorators import ratelimit
from django.views.decorators.csrf import csrf_exempt

# Limit anonymous users: 5 requests/minute
# Limit authenticated users: 10 requests/minute

@csrf_exempt
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
@ratelimit(key='user_or_ip', rate='10/m', method='POST', block=True)



def login_view(request):
    """
    Example login view protected by rate limiting.
    """
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        return JsonResponse({'error': 'Too many requests, please try again later.'}, status=429)

    # Your login logic here
    return JsonResponse({'message': 'Login successful!'})


def user_or_ip(request):
    if request.user.is_authenticated:
        return str(request.user.id)
    return request.META.get("REMOTE_ADDR")

@csrf_exempt
@ratelimit(key=user_or_ip, rate='10/m', method='POST', block=False)
@ratelimit(key='ip', rate='5/m', method='POST', block=False)
def login_view(request):
    """
    Login view protected by rate limiting.
    """
    # Check rate limiting
    if getattr(request, 'limited', False):
        return JsonResponse(
            {"error": "Too many requests, please try again later."}, status=429
        )

    # Your login logic here (authentication, session, token, etc.)
    return JsonResponse({"message": "Login successful!"})