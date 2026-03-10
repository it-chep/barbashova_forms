import os
import re

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import SuspiciousFileOperation
from django.db import models


def safe_filename(filename):
    filename = re.sub(r"[^\w\s.-]", "", filename).strip()
    if ".." in filename or filename.startswith("/"):
        raise SuspiciousFileOperation("Detected path traversal attempt")
    return filename


class BusinessForm(models.Model):
    def get_upload_photo_path(self, filename):
        filename = safe_filename(filename)
        return os.path.join("banners", filename)

    def get_upload_spasibo_path(self, filename):
        filename = safe_filename(filename)
        return os.path.join("spasibo", filename)

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    photo = models.ImageField(upload_to=get_upload_photo_path)
    spasibo_photo = models.ImageField(upload_to=get_upload_spasibo_path)

    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Конфигурации форм"
        verbose_name_plural = "Конфигурации форм"


class NewProduct(models.Model):
    SOURCE_CHOICES = [
        ("instagram", "Instagram"),
        ("telegram", "Telegram"),
    ]

    MRI_EXPERIENCE_CHOICES = [
        ("0-1_year", "0-1 год"),
        ("2-5_years", "2-5 лет"),
        ("resident_student", "я ординатор/студент"),
        ("other", "Другое"),
    ]

    SPECIALIZATION_CHOICES = [
        ("radiologist", "рентгенолог"),
        ("resident_student", "я ординатор/студент"),
    ]

    MRI_DESCRIPTION_EXPERIENCE_CHOICES = [
        ("no", "Нет"),
        ("yes", "Да"),
    ]

    WORK_SCHEDULE_CHOICES = [
        ("until_14", "до 14.00"),
        ("14_to_20", "с 14.00 до 20.00"),
        ("night_shifts", "Ночные дежурства"),
    ]

    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        verbose_name="Вы увидели эту анкету у меня в:",
    )
    mri_experience = models.CharField(
        max_length=30,
        choices=MRI_EXPERIENCE_CHOICES,
        verbose_name="Ваш опыт в МРТ",
    )
    mri_experience_other = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Ваш опыт в МРТ: другое",
    )
    specialization = models.CharField(
        max_length=30,
        choices=SPECIALIZATION_CHOICES,
        verbose_name="Ваша специальность",
    )
    mri_description_experience = models.TextField(
        verbose_name="У вас есть опыт описания МРТ",
    )
    mri_description_experience_details = models.TextField(
        blank=True,
        verbose_name="укажите количество лет",
    )
    city = models.CharField(
        max_length=120,
        verbose_name="Город проживания в настоящий момент (для понимания часового пояса)",
    )
    income_rub = models.CharField(
        max_length=120,
        verbose_name="Вас средний доход в месяц, в рублях",
    )
    difficult_sections = models.TextField(
        verbose_name="Какие разделы в МРТ у вас вызывают наибольшие трудности",
    )
    can_plan_mri = models.TextField(
        verbose_name="Вы умеете самостоятельно планировать МРТ исследования",
    )
    work_schedule = models.CharField(
        max_length=20,
        choices=WORK_SCHEDULE_CHOICES,
        verbose_name="Ваш график работы",
    )
    convenient_time = models.TextField(
        verbose_name="Укажите удобное время для прохождения курса",
    )
    convenient_weekdays = models.TextField(
        verbose_name="Укажите удобные дни недели для прохождения курса",
    )
    full_name = models.CharField(
        max_length=200,
        verbose_name="Укажите ваше ФИО",
    )
    phone = models.CharField(
        max_length=30,
        verbose_name="Ваш номер телефона",
    )
    telegram = models.CharField(
        max_length=200,
        verbose_name="Ваш личный ник в телеграм для связи",
    )
    policy_agreement = models.BooleanField(
        default=False,
        verbose_name="Согласен с политикой обработки персональных данных",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Анкета предзаписи для рентгенологов"
        verbose_name_plural = "Анкеты предзаписи для рентгенологов"

    def __str__(self):
        return f"Анкета от {self.full_name}"
