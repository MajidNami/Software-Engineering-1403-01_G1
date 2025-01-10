from django.shortcuts import render
from django.http import JsonResponse
from .services import DictionaryAPI

# Create your views here.
def home(request):
    return render (request , 'group5.html' , {'group_number': '5'})


def dictionary(request, word):
    if request.method == "GET":
        word = DictionaryAPI.getInstance().fetch_word(word)
        if word is None:
            return JsonResponse({"error": "Word not found"}, status=404)
        
        return JsonResponse(word.to_dict())
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)