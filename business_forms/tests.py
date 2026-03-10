from django.test import SimpleTestCase

from business_forms.forms import NewProductForm


class NewProductFormTests(SimpleTestCase):
    def get_valid_data(self):
        return {
            "source": "instagram",
            "mri_experience": "0-1_year",
            "specialization": "radiologist",
            "mri_description_experience": "no",
            "city": "Москва",
            "income_rub": "150000",
            "difficult_sections": "МРТ позвоночника",
            "can_plan_mri": "Частично",
            "work_schedule": "until_14",
            "convenient_time": "вечером",
            "convenient_weekdays": "вторник и четверг",
            "full_name": "Иван Иванов",
            "phone": "+79990000000",
            "telegram": "@username",
            "policy_agreement": "on",
        }

    def test_requires_other_text_for_other_mri_experience(self):
        data = self.get_valid_data()
        data["mri_experience"] = "other"

        form = NewProductForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("mri_experience_other", form.errors)

    def test_requires_details_when_yes_selected_for_description_experience(self):
        data = self.get_valid_data()
        data["mri_description_experience"] = "yes"

        form = NewProductForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("mri_description_experience_details", form.errors)

    def test_joins_checkbox_values_on_save(self):
        data = self.get_valid_data()
        data["mri_description_experience"] = "yes"
        data["mri_description_experience_details"] = "2 года"

        form = NewProductForm(data=data)

        self.assertTrue(form.is_valid(), form.errors)
        instance = form.save(commit=False)
        self.assertEqual(instance.mri_description_experience, "yes")
        self.assertEqual(instance.mri_description_experience_details, "2 года")
