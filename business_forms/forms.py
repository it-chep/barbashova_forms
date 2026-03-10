from django import forms

from .models import NewProduct


class NewProductForm(forms.ModelForm):
    class Meta:
        model = NewProduct
        fields = (
            "source",
            "specialization",
            "specialization_other",
            "mri_experience",
            "mri_experience_other",
            "difficult_sections",
            "income_rub",
            "can_plan_mri",
            "work_schedule",
            "work_schedule_other",
            "convenient_time",
            "convenient_weekdays",
            "city",
            "full_name",
            "phone",
            "telegram",
            "policy_agreement",
        )
        widgets = {
            "source": forms.RadioSelect,
            "specialization": forms.RadioSelect,
            "mri_experience": forms.RadioSelect,
            "work_schedule": forms.RadioSelect,
            "specialization_other": forms.TextInput(attrs={"placeholder": "Мой ответ"}),
            "mri_experience_other": forms.TextInput(attrs={"placeholder": "Мой ответ"}),
            "work_schedule_other": forms.TextInput(attrs={"placeholder": "Мой ответ"}),
            "difficult_sections": forms.Textarea(attrs={"placeholder": "Мой ответ", "class": "auto-resize-textarea", "rows": 1}),
            "income_rub": forms.TextInput(attrs={"placeholder": "Мой ответ"}),
            "can_plan_mri": forms.Textarea(attrs={"placeholder": "Мой ответ", "class": "auto-resize-textarea", "rows": 1}),
            "convenient_time": forms.Textarea(attrs={"placeholder": "Мой ответ", "class": "auto-resize-textarea", "rows": 1}),
            "convenient_weekdays": forms.Textarea(attrs={"placeholder": "Мой ответ", "class": "auto-resize-textarea", "rows": 1}),
            "city": forms.TextInput(attrs={"placeholder": "Мой ответ"}),
            "full_name": forms.TextInput(attrs={"placeholder": "Мой ответ"}),
            "phone": forms.TextInput(attrs={"placeholder": "+7 (999) 999-99-99"}),
            "telegram": forms.TextInput(attrs={"placeholder": "@username"}),
            "policy_agreement": forms.CheckboxInput(attrs={"style": "display:none"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["source"].choices = list(NewProduct.SOURCE_CHOICES)
        self.fields["specialization"].choices = list(NewProduct.SPECIALIZATION_CHOICES)
        self.fields["mri_experience"].choices = list(NewProduct.MRI_EXPERIENCE_CHOICES)
        self.fields["work_schedule"].choices = list(NewProduct.WORK_SCHEDULE_CHOICES)

        for field_name, field in self.fields.items():
            field.required = field_name not in {"specialization_other", "mri_experience_other", "work_schedule_other"}
            field.error_messages.update({"required": "Обязательное поле"})

        self.fields["specialization_other"].widget.attrs.update({"disabled": True, "data-other-input": "specialization"})
        self.fields["mri_experience_other"].widget.attrs.update({"disabled": True, "data-other-input": "mri_experience"})
        self.fields["work_schedule_other"].widget.attrs.update({"disabled": True, "data-other-input": "work_schedule"})

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("specialization") == "other" and not cleaned_data.get("specialization_other", "").strip():
            self.add_error("specialization_other", "Обязательное поле")
        if cleaned_data.get("mri_experience") == "other" and not cleaned_data.get("mri_experience_other", "").strip():
            self.add_error("mri_experience_other", "Обязательное поле")
        if cleaned_data.get("work_schedule") == "other" and not cleaned_data.get("work_schedule_other", "").strip():
            self.add_error("work_schedule_other", "Обязательное поле")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.specialization != "other":
            instance.specialization_other = ""
        if instance.mri_experience != "other":
            instance.mri_experience_other = ""
        if instance.work_schedule != "other":
            instance.work_schedule_other = ""
        if commit:
            instance.save()
        return instance
