import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app01.utils import react_search_spotify


@csrf_exempt
def react_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            print(email, password)

            if email == "123" and password == "123":
                return JsonResponse({'message': 'Login successful', 'access': 'dummy_token'})
            else:
                return JsonResponse({'error': 'Incorrect email or password'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def react_user_profile(request):
    return JsonResponse({'id': '1234567890', 'message': 'Hello baby'})


def react_search_result(request):
    query = request.GET.get('query', '')
    results = react_search_spotify.search_spotify(query)
    return JsonResponse(results, safe=False)

