from django.shortcuts import render

def index(request):
  context = {
    # Put some render context here
  }
  return render(request, "frontend/index.html", context)
