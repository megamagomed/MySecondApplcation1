from django.shortcuts import render, redirect
from .models import Account, Chat
from django.http import Http404
from .forms import (
    CreateUserForm,
    LoginUserForm,
    EditProfileForm,
    CreateProfileModelForm,
    ChatForm,
)
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError


def profiles_list(request):
    list_obj = Account.objects.all()
    list_obj = list_obj.exclude(user=request.user.id)
    return render(request, "accounts/list.html", {"list_obj": list_obj})


def profile_settings(request, pk):
    try:
        obj = Account.objects.get(id=pk)
    except Account.DoesNotExist:
        raise Http404

    chat_form = ChatForm()

    all_likes = obj.like.all()

    final_qs = {}

    for user in all_likes:
        user_likes = user.account_user.like.all()

        if obj.user in user_likes and obj.user != user:
            sender_messages = Chat.objects.filter(sender=obj.user, receiver=user)
            receiver_messages = Chat.objects.filter(sender=user, receiver=obj.user)
            final_qs[user] = sender_messages.union(receiver_messages)

    if request.method == "POST":
        chat_form = ChatForm(request.POST)
        if chat_form.is_valid():
            print(chat_form.cleaned_data)
            chat_text = chat_form.cleaned_data["chat_text"]
            sender = User.objects.get(id=request.user.id)
            reciever = chat_form.data["reciever"][0]
            reciever_user = User.objects.get(id=reciever)
            Chat.objects.create(
                sender=sender, receiver=reciever_user, message=chat_text
            )
            return redirect(f"/accounts/{pk}")

    return render(
        request,
        "accounts/profile.html",
        {"profile": obj, "chat_form": chat_form, "chat_qs": final_qs},
    )


def user_create(request):
    if request.method == "GET":
        form = CreateUserForm()
        return render(request, "accounts/user_create.html", {"form": form})

    elif request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            User.objects.create_user(
                username=name, email=email, password=password
            ).save()

        return redirect("/accounts/login/")


def user_edit(request, pk):
    print(request.POST)
    current_user = Account.objects.get(id=pk)
    if current_user.user != request.user:
        raise Http404("Отвали самозванец")
    if request.method == "GET":
        form = CreateProfileModelForm(instance=current_user)
        return render(request, "accounts/user_edit.html", {"form": form})
    elif request.method == "POST":
        form = CreateProfileModelForm(
            request.POST, request.FILES, instance=current_user
        )

        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect(f"/accounts/{current_user.id}/")


def user_login(request):
    if request.method == "GET":
        form = LoginUserForm()
        return render(request, "accounts/user_login.html", {"form": form})

    elif request.method == "POST":
        form = LoginUserForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            password = form.cleaned_data["password"]
            user = authenticate(username=name, password=password)
            if user:
                login(request, user)
                return redirect("/accounts/create/")

        return render(request, "accounts/user_login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("/accounts/login/")


def user_delete(request, pk):
    if Account.objects.get(id=pk).user != request.user:
        raise Http404("Отвали самозванец")
    try:
        obj = Account.objects.get(id=pk)
    except Account.DoesNotExist:
        raise Http404

    return render(request, "accounts/delete_profile.html", {"profile": obj})


def confirm_user_delete(request, pk):
    current_user = Account.objects.get(id=pk)
    if current_user.user != request.user:
        raise Http404("Отвали самозванец")
    try:
        obj = Account.objects.get(id=pk)
    except Account.DoesNotExist:
        raise Http404

    obj.delete()
    return redirect("/accounts/")


@login_required
def profile_create(request):
    if request.method == "GET":
        form = CreateProfileModelForm()
        return render(request, "accounts/profile_create.html", {"form": form})

    elif request.method == "POST":
        form = CreateProfileModelForm(request.POST, request.FILES)

        if form.is_valid():
            form = form.save(commit=False)
            user = request.user
            form.user = user
            form.save()
        return redirect(f"/accounts/{user.account_user.pk}/")


def like_view(request, pk):
    self_account = request.user.account_user  # это аккаунт того, кто лайкает
    other_account = Account.objects.get(id=pk).user
    self_account.like.add(other_account)

    return redirect(f"/accounts/{pk}")
