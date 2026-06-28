from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


MAX_NAME_LENGTH = 124
MAX_SURNAME_LENGTH = 124
MAX_PHONE_LENGTH = 20
MAX_ABOUT_LENGTH = 256


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, name, surname, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, surname=surname, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, name, surname, password, **extra_fields)


class User(AbstractUser):
    username = None

    email = models.EmailField("Email", unique=True)
    name = models.CharField("Имя", max_length=MAX_NAME_LENGTH)
    surname = models.CharField("Фамилия", max_length=MAX_SURNAME_LENGTH)
    avatar = models.ImageField("Аватар", upload_to="avatars/", blank=True, default="")
    phone = models.CharField("Телефон", max_length=MAX_PHONE_LENGTH, blank=True, default="")
    github_url = models.URLField("GitHub", blank=True, default="")
    about = models.CharField("О себе", max_length=MAX_ABOUT_LENGTH, blank=True, default="")
    favorites = models.ManyToManyField(
        "projects.Project",
        related_name="interested_users",
        blank=True,
        verbose_name="Избранные проекты",
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        ordering = ["id"]

    def __str__(self):
        return f"{self.name} {self.surname} <{self.email}>"
