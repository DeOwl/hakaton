from django.shortcuts import render

# Create your views here.
def example(request):
    return render(request, 'example.html',         
                  {'example': 'This is an example of a Django view.'}, 
                  )