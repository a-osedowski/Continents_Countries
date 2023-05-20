from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView


def home(request):
    if request.method == 'POST':
        continent = request.POST.get('continent')
        number = request.POST.get('number')

        # Do something with the continent and number values
        # For example, you can save them to a database or perform any desired processing

        return HttpResponse('Form submitted successfully!')
    return render(request, 'home.html')

# class PostContinentFromUser(CreateView):
#     template_name = 'home.html'
#     # fields = ['continent', 'number']
#     def get_queryset(self):




