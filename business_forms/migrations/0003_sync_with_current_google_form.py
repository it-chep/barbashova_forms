from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("business_forms", "0002_newproduct_mri_description_experience_details"),
    ]

    operations = [
        migrations.AddField(
            model_name="newproduct",
            name="specialization_other",
            field=models.CharField(blank=True, max_length=255, verbose_name="Ваша специальность: другое"),
        ),
        migrations.AddField(
            model_name="newproduct",
            name="work_schedule_other",
            field=models.CharField(blank=True, max_length=255, verbose_name="Ваш график работы: другое"),
        ),
        migrations.RemoveField(
            model_name="newproduct",
            name="mri_description_experience",
        ),
        migrations.RemoveField(
            model_name="newproduct",
            name="mri_description_experience_details",
        ),
        migrations.AlterField(
            model_name="newproduct",
            name="specialization",
            field=models.CharField(choices=[("radiologist", "рентгенолог"), ("resident_student", "я ординатор/студент"), ("other", "Другое")], max_length=30, verbose_name="Ваша специальность"),
        ),
        migrations.AlterField(
            model_name="newproduct",
            name="city",
            field=models.CharField(max_length=120, verbose_name="Город проживания в настоящий момент"),
        ),
        migrations.AlterField(
            model_name="newproduct",
            name="can_plan_mri",
            field=models.TextField(verbose_name="Вы умеете самостоятельно планировать МРТ исследования?"),
        ),
        migrations.AlterField(
            model_name="newproduct",
            name="work_schedule",
            field=models.CharField(choices=[("until_14", "до 14.00"), ("14_to_20", "с 14.00 до 20.00"), ("night_shifts", "Ночные дежурства"), ("other", "Другое")], max_length=20, verbose_name="Ваш график работы"),
        ),
    ]
