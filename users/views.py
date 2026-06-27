from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LoginForm, ProfileEditForm, RegisterForm
from .models import User


def _get_query_prefix(request):
    params = request.GET.copy()
    params.pop("page", None)
    query_string = params.urlencode()
    return query_string + "&" if query_string else ""


def register_view(request):
    if request.user.is_authenticated:
        return redirect("projects:list")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("projects:list")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("projects:list")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            login(request, user)
            return redirect("projects:list")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("projects:list")


def users_list(request):
    queryset = User.objects.order_by("id")
    active_filter = request.GET.get("filter")
    if request.user.is_authenticated and active_filter:
        if active_filter == "owners-of-favorite-projects":
            queryset = queryset.filter(owned_projects__in=request.user.favorites.all())
        elif active_filter == "owners-of-participating-projects":
            queryset = queryset.filter(owned_projects__participants=request.user)
        elif active_filter == "interested-in-my-projects":
            queryset = queryset.filter(favorites__owner=request.user)
        elif active_filter == "participants-of-my-projects":
            queryset = queryset.filter(participated_projects__owner=request.user)
        queryset = queryset.distinct().order_by("id")

    paginator = Paginator(queryset, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "users/participants.html",
        {
            "page_obj": page_obj,
            "active_filter": active_filter,
            "query_prefix": _get_query_prefix(request),
        },
    )


def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, "users/user-details.html", {"user": user})


@login_required(login_url="/users/login/")
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("users:detail", pk=user.pk)
    else:
        form = ProfileEditForm(instance=user)
    return render(request, "users/edit_profile.html", {"form": form, "user": user})


@login_required(login_url="/users/login/")
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("users:detail", pk=request.user.pk)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "users/change_password.html", {"form": form})
