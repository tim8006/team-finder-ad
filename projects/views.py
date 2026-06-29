from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from team_finder.utils import get_query_prefix, paginate_queryset

from .forms import ProjectForm
from .models import Project


def project_list(request):
    queryset = Project.objects.select_related("owner").prefetch_related("participants")
    page_obj = paginate_queryset(queryset, request)
    favorite_project_ids = set(request.user.favorites.values_list("pk", flat=True)) if request.user.is_authenticated else set()
    return render(
        request,
        "projects/project_list.html",
        {
            "page_obj": page_obj,
            "projects": page_obj.object_list,
            "query_prefix": get_query_prefix(request),
            "favorite_project_ids": favorite_project_ids,
        },
    )


@login_required(login_url="/users/login/")
def favorite_projects(request):
    projects = request.user.favorites.select_related("owner").prefetch_related("participants").all()
    favorite_project_ids = set(projects.values_list("pk", flat=True))
    return render(
        request,
        "projects/favorite_projects.html",
        {"projects": projects, "favorite_project_ids": favorite_project_ids},
    )


def project_detail(request, pk):
    project = get_object_or_404(
        Project.objects.select_related("owner").prefetch_related("participants"),
        pk=pk,
    )
    favorite_project_ids = set(request.user.favorites.values_list("pk", flat=True)) if request.user.is_authenticated else set()
    is_participant = (
        request.user.is_authenticated
        and project.participants.filter(pk=request.user.pk).exists()
    )
    return render(
        request,
        "projects/project-details.html",
        {
            "project": project,
            "favorite_project_ids": favorite_project_ids,
            "is_participant": is_participant,
        },
    )


@login_required(login_url="/users/login/")
def project_create(request):
    form = ProjectForm(request.POST or None)
    if request.method != "POST" or not form.is_valid():
        return render(request, "projects/create-project.html", {"form": form, "is_edit": False})

    project = form.save(commit=False)
    project.owner = request.user
    project.save()
    project.participants.add(request.user)
    return redirect("projects:detail", pk=project.pk)


@login_required(login_url="/users/login/")
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.owner != request.user:
        return redirect("projects:detail", pk=project.pk)

    form = ProjectForm(request.POST or None, instance=project)
    if request.method != "POST" or not form.is_valid():
        return render(request, "projects/create-project.html", {"form": form, "is_edit": True})

    form.save()
    return redirect("projects:detail", pk=project.pk)


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
    is_participant = project.participants.filter(pk=request.user.pk).exists()
    if is_participant:
        project.participants.remove(request.user)
        participant = False
    else:
        project.participants.add(request.user)
        participant = True
    return JsonResponse({"status": "ok", "participant": participant})
