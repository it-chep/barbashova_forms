from django import forms

from .models import NewProduct


class NewProductForm(forms.ModelForm):
    class Meta:
        model = NewProduct
        fields = (
            "source",
            "mri_experience",
            "mri_experience_other",
            "specialization",
            "mri_description_experience",
            "mri_description_experience_details",
            "city",
            "income_rub",
            "difficult_sections",
            "can_plan_mri",
            "work_schedule",
            "convenient_time",
            "convenient_weekdays",
            "full_name",
            "phone",
            "telegram",
            "policy_agreement",
        )
        widgets = {
            "source": forms.RadioSelect,
            "mri_experience": forms.RadioSelect,
            "specialization": forms.RadioSelect,
            "mri_description_experience": forms.RadioSelect,
            "work_schedule": forms.RadioSelect,
            "mri_experience_other": forms.TextInput(attrs={"placeholder": "Мой ответ"}),
            "mri_description_experience_details": forms.Textarea(
                attrs={"placeholder": "впишите сколько лет", "class": "auto-resize-textarea", "rows": 1}
            ),
            "city": forms.TextInput(attrs={"placeholder": "Мой ответ"}),
            "income_rub": forms.TextInput(attrs={"placeholder": "Мой ответ"}),
            "difficult_sections": forms.Textarea(attrs={"placeholder": "Мой ответ", "class": "auto-resize-textarea", "rows": 1}),
            "can_plan_mri": forms.Textarea(attrs={"placeholder": "Мой ответ", "class": "auto-resize-textarea", "rows": 1}),
            "convenient_time": forms.Textarea(attrs={"placeholder": "Мой ответ", "class": "auto-resize-textarea", "rows": 1}),
            "convenient_weekdays": forms.Textarea(attrs={"placeholder": "Мой ответ", "class": "auto-resize-textarea", "rows": 1}),
            "full_name": forms.TextInput(attrs={"placeholder": "Мой ответ"}),
            "phone": forms.TextInput(attrs={"placeholder": "+7 (999) 999-99-99"}),
            "telegram": forms.TextInput(attrs={"placeholder": "@username"}),
            "policy_agreement": forms.CheckboxInput(attrs={"style": "display:none"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["source"].choices = list(NewProduct.SOURCE_CHOICES)
        self.fields["mri_experience"].choices = list(NewProduct.MRI_EXPERIENCE_CHOICES)
        self.fields["specialization"].choices = list(NewProduct.SPECIALIZATION_CHOICES)
        self.fields["mri_description_experience"].choices = list(NewProduct.MRI_DESCRIPTION_EXPERIENCE_CHOICES)
        self.fields["work_schedule"].choices = list(NewProduct.WORK_SCHEDULE_CHOICES)

        for field_name, field in self.fields.items():
            field.required = field_name not in {"mri_experience_other", "mri_description_experience_details"}
            field.error_messages.update({"required": "Обязательное поле"})

        self.fields["mri_experience_other"].widget.attrs.update(
            {"disabled": True, "data-other-input": "mri_experience"}
        )
        self.fields["mri_description_experience_details"].widget.attrs.update(
            {"disabled": True, "data-other-input": "mri_description_experience"}
        )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("mri_experience") == "other" and not cleaned_data.get("mri_experience_other", "").strip():
            self.add_error("mri_experience_other", "Обязательное поле")
        if cleaned_data.get("mri_description_experience") == "yes" and not cleaned_data.get("mri_description_experience_details", "").strip():
            self.add_error("mri_description_experience_details", "Обязательное поле")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.mri_experience != "other":
            instance.mri_experience_other = ""
        if self.cleaned_data["mri_description_experience"] != "yes":
            instance.mri_description_experience_details = ""
        if commit:
            instance.save()
        return instance
