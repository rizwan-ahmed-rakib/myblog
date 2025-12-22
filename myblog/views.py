from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import HttpResponseRedirect

def index(request):
    return HttpResponseRedirect(reverse('my_blog:blog_list'))

