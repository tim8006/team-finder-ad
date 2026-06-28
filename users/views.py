from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404, redirect, render

from team_finder.utils import get_query_prefix, paginate_queryset

from .forms import LoginForm, ProfileEditForm, RegisterForm
from .models import User

FILTER_OWNERS_OF_FAVORITE_PROJECTS = "owners-of-favorite-projects"
FILTER_OWNERS_OF_PARTICIPATING_PROJECTS = "owners-of-participating-projects"
FILTER_INTERESTED_IN_MY_PROJECTS = "interested-in-my-projects"
FILTER_PARTICIPANTS_OF_MY_PROJECTS = "participants-of-my-projects"


def register_view(request):
    if request.user.is_authenticated:
        return redirect("projects:list")

    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("projects:list")

    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("projects:list")

    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.cleaned_data["user"]
        login(request, user)
        return redirect("projects:list")

    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("projects:list")


def users_list(request):
    queryset = User.objects.all()
    active_filter = request.GET.get("filter")
    if request.user.is_authenticated and active_filter:
        if active_filter == FILTER_OWNERS_OF_FAVORITE_PROJECTS:
            queryset = queryset.filter(owned_projects__in=request.user.favorites.all())
        elif active_filter == FILTER_OWNERS_OF_PARTICIPATING_PROJECTS:
            queryset = queryset.filter(owned_projects__participants=request.user)
        elif active_filter == FILTER_INTERESTED_IN_MY_PROJECTS:
            queryset = queryset.filter(favorites__owner=request.user)
        elif active_filter == FILTER_PARTICIPANTS_OF_MY_PROJECTS:
            queryset = queryset.filter(participated_projects__owner=request.user)
        queryset = queryset.distinct()

    page_obj = paginate_queryset(queryset, request)
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
    form = ProfileEditForm(request.POST or None, request.FILES or None, instance=user)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("users:detail", pk=user.pk)
    return render(request, "users/edit_profile.html", {"form": form, "user": user})


@login_required(login_url="/users/login/")
def change_password(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        return redirect("users:detail", pk=request.user.pk)
    return render(request, "users/change_password.html", {"form": form})
