from .tasks import run
from django.http import JsonResponse

# Create your views here.


def run_bot(request):
    res = run()
    return JsonResponse(res)


def say_hello(request):
    return JsonResponse({'message': 'Hello, world!'})
