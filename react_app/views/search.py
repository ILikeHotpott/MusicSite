from django.http import JsonResponse
from app01.utils import react_search_spotify


def react_search_result(request):
    query = request.GET.get('query', '')
    results = react_search_spotify.search_spotify(query)
    return JsonResponse(results, safe=False)