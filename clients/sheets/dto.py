from dataclasses import dataclass
from typing import Optional


@dataclass
class NewProductData:
    source: Optional[str] = None
    specialization: Optional[str] = None
    mri_experience: Optional[str] = None
    mri_experience_other: Optional[str] = None
    difficult_sections: Optional[str] = None
    income_rub: Optional[str] = None
    can_plan_mri: Optional[str] = None
    work_schedule: Optional[str] = None
    convenient_time: Optional[str] = None
    convenient_weekdays: Optional[str] = None
    city: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    telegram: Optional[str] = None
    policy_agreement: bool = False

    @classmethod
    def from_model(cls, model_instance) -> "NewProductData":
        specialization = model_instance.get_specialization_display()
        if model_instance.specialization == "other":
            specialization = model_instance.specialization_other

        mri_experience = model_instance.get_mri_experience_display()
        if model_instance.mri_experience == "other":
            mri_experience = model_instance.mri_experience_other

        work_schedule = model_instance.get_work_schedule_display()
        if model_instance.work_schedule == "other":
            work_schedule = model_instance.work_schedule_other

        return cls(
            source=model_instance.get_source_display(),
            specialization=specialization,
            mri_experience=mri_experience,
            difficult_sections=model_instance.difficult_sections,
            income_rub=model_instance.income_rub,
            can_plan_mri=model_instance.can_plan_mri,
            work_schedule=work_schedule,
            convenient_time=model_instance.convenient_time,
            convenient_weekdays=model_instance.convenient_weekdays,
            city=model_instance.city,
            full_name=model_instance.full_name,
            phone=model_instance.phone,
            telegram=model_instance.telegram,
            policy_agreement=model_instance.policy_agreement,
            mri_experience_other=model_instance.mri_experience_other,
        )
