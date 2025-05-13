from django.shortcuts import render,redirect,get_object_or_404
from lists.forms import ItemForm,ExistingListItemForm
from lists.models import Item,List
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.mail import send_mail

User = get_user_model()

def home_page(request):
    return render(request,'home.html',{"form":ItemForm()})
    

def new_list(request):
    form  = ItemForm(data=request.POST)
    if form.is_valid():
        nulist = List.objects.create()
        if request.user.is_authenticated:
            nulist.owner = request.user
            nulist.save()
        form.save(for_list=nulist)
        return redirect(nulist)
    else:
        return render(request,"home.html",{"form":form})


def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    if request.method == "POST":
        form = ExistingListItemForm(for_list=our_list, data=request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user if request.user.is_authenticated else None
            item.save()
            return redirect(our_list)
    else:
        form = ExistingListItemForm(for_list=our_list)
    return render(request, "list.html", {"list": our_list, "form": form})


def my_lists(request,email):
    owner = User.objects.get(email=email)
    lists = List.objects.filter(owner=owner) | owner.shared_lists.all()
    return render(request, 'my_lists.html', {'owner': owner, 'lists': lists})



def share_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    sharee_email = request.POST.get('sharee', '').strip().lower()

    if sharee_email:
        try:
            user_to_share = User.objects.get(email=sharee_email)
            list_.shared_with.add(user_to_share)
            
            if request.user.is_authenticated:
                # Send email notification
                send_mail(
                    subject="Superlists: A To-Do list has been shared with you",
                    message=f"{request.user.email} has shared a to-do list with you. View it here: {request.build_absolute_uri(list_.get_absolute_url())}",
                    from_email='jyotichetry087@gmail.com',
                    recipient_list=[sharee_email],
                    fail_silently=False,
                )
                messages.success(request, f"List shared with {sharee_email}")
            else:
                messages.warning(request, "You must be logged in to send share notifications.")

        except User.DoesNotExist:
            messages.error(request, f"No such user with email: {sharee_email}")

    return redirect(list_)
