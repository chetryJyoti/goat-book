from django.shortcuts import render,redirect
from lists.forms import ItemForm,ExistingListItemForm
from lists.models import Item,List

def home_page(request):
    return render(request,'home.html',{"form":ItemForm()})
    

def new_list(request):
    form  = ItemForm(data=request.POST)
    if form.is_valid():
        nulist = List.objects.create()
        # Item.objects.create(text=request.POST['text'],list=nulist)
        form.save(for_list=nulist)
        return redirect(nulist)
    else:
        return render(request,"home.html",{"form":form})


def view_list(request,list_id):
    our_list = List.objects.get(id=list_id)
    if request.method == "POST":
        form = ExistingListItemForm(for_list=our_list,data=request.POST)
        if form.is_valid():
            # Item.objects.create(text=request.POST['text'],list=our_list)
            form.save()
            return redirect(our_list)
    else:
        form = ExistingListItemForm(for_list=our_list)
    return render(request,"list.html",{"list":our_list,"form":form})