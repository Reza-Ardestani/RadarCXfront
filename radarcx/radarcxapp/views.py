from django.shortcuts import render

def coinlist(request):
    return render(request, 'result.html')