from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("business_forms", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="newproduct",
            name="mri_description_experience_details",
            field=models.TextField(blank=True, verbose_name="впишите сколько лет"),
        ),
    ]
