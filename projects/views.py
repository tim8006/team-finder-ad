from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProjectForm
from .models import Project


def _get_query_prefix(request):
    params = request.GET.copy()
    params.pop("page", None)
    query_string = params.urlencode()
    return query_string + "&" if query_string else ""


def project_list(request):
    queryset = Project.objects.all()
    paginator = Paginator(queryset, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "projects/project_list.html",
        {"page_obj": page_obj, "projects": page_obj.object_list, "query_prefix": _get_query_prefix(request)},
    )


@login_required(login_url="/users/login/")
def favorite_projects(request):
    projects = request.user.favorites.all()
    return render(request, "projects/favorite_projects.html", {"projects": projects})


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, "projects/project-details.html", {"project": project})


@login_required(login_url="/users/login/")
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            project.participants.add(request.user)
            return redirect("projects:detail", pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, "projects/create-project.html", {"form": form, "is_edit": False})


@login_required(login_url="/users/login/")
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.owner != request.user:
        return redirect("projects:detail", pk=project.pk)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("projects:detail", pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, "projects/create-project.html", {"form": form, "is_edit": True})


@login_required(login_url="/users/login/")
def toggle_favorite(request, pk):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Метод не поддерживается"}, status=405)
    project = get_object_or_404(Project, pk=pk)
    if request.user.favorites.filter(pk=project.pk).exists():
        request.user.favorites.remove(project)
        favorited = False
    else:
        request.user.favorites.add(project)
        favorited = True
    return JsonResponse({"status": "ok", "favorited": favorited})


@login_required(login_url="/users/login/")
def complete_project(request, pk):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Метод не поддерживается"}, status=405)
    project = get_object_or_404(Project, pk=pk)
    if project.owner != request.user or project.status != Project.STATUS_OPEN:
        return JsonResponse({"status": "error", "message": "Нет прав или проект уже завершён"}, status=403)
    project.status = Project.STATUS_CLOSED
    project.save()
    return JsonResponse({"status": "ok", "project_status": project.status})


@login_required(login_url="/users/login/")
def toggle_participate(request, pk):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Метод не поддерживается"}, status=405)
    project = get_object_or_404(Project, pk=pk)
    if request.user in project.participants.all():
        project.participants.remove(request.user)
        participant = False
    else:
        project.participants.add(request.user)
        participant = True
    return JsonResponse({"status": "ok", "participant": participant})
