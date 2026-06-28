from django.conf import settings
from django.db import models

from .constants import MAX_PROJECT_NAME_LENGTH, MAX_PROJECT_STATUS_LENGTH


class Project(models.Model):
    STATUS_OPEN = "open"
    STATUS_CLOSED = "closed"
    STATUS_CHOICES = [
        (STATUS_OPEN, "Открыт"),
        (STATUS_CLOSED, "Закрыт"),
    ]

    name = models.CharField("Название проекта", max_length=MAX_PROJECT_NAME_LENGTH)
    description = models.TextField("Описание проекта", blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects",
        verbose_name="Владелец проекта",
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    github_url = models.URLField("GitHub URL", blank=True)
    status = models.CharField(
        "Статус проекта",
        max_length=MAX_PROJECT_STATUS_LENGTH,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN,
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="participated_projects",
        blank=True,
        verbose_name="Участники проекта",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "проект"
        verbose_name_plural = "проекты"

    def __str__(self):
        return self.name
