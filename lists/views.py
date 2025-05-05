from django.shortcuts import render
from django.http import HttpResponse


def home_page(request):
    # if request.method == "POST":
    #     return HttpResponse("You submitted:"+request.POST["item_text"])
    return render(request,'home.html',{'new_item_text' : request.POST.get("item_text","")})