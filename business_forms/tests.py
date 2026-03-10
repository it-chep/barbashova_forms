from django.test import SimpleTestCase

from business_forms.forms import NewProductForm


class NewProductFormTests(SimpleTestCase):
    def get_valid_data(self):
        return {
            "source": "instagram",
            "specialization": "radiologist",
            "mri_experience": "0-1_year",
            "difficult_sections": "МРТ позвоночника",
            "income_rub": "150000",
            "can_plan_mri": "Частично",
            "work_schedule": "until_14",
            "convenient_time": "вечером",
            "convenient_weekdays": "вторник и четверг",
            "city": "Москва",
            "full_name": "Иван Иванов",
            "phone": "+79990000000",
            "telegram": "@username",
            "policy_agreement": "on",
        }

    def test_requires_other_text_for_other_specialization(self):
        data = self.get_valid_data()
        data["specialization"] = "other"

        form = NewProductForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("specialization_other", form.errors)

    def test_requires_other_text_for_other_mri_experience(self):
        data = self.get_valid_data()
        data["mri_experience"] = "other"

        form = NewProductForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("mri_experience_other", form.errors)

    def test_requires_other_text_for_other_work_schedule(self):
        data = self.get_valid_data()
        data["work_schedule"] = "other"

        form = NewProductForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("work_schedule_other", form.errors)
