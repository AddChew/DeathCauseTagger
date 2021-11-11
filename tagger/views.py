from django.shortcuts import render
# from django.http import HttpResponseRedirect
# from django.urls import reverse


# Upload Page
def upload(request):
    return render(request, "tagger/upload.html")