from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_appointment.constants import NEW_APPT

from .karabo_screening_model_wrapper import KaraboSubjectScreeningModelWrapper


class KaraboScreeningModelWrapperMixin:

    karabo_screening_model_wrapper_cls = KaraboSubjectScreeningModelWrapper

    karabo_subject_screening_cls = django_apps.get_model(
        'td_maternal.karabosubjectscreening')

    infant_appointment_cls = django_apps.get_model(
        'td_infant.appointment')

    @property
    def karabo_subject_screening_obj(self):
        """Returns a karabo subject screening model instance or None.
        """
        try:
            return self.karabo_subject_screening_cls.objects.get(
                subject_identifier=self.subject_identifier)
        except ObjectDoesNotExist:
            return None

    @property
    def karabo_subject_screening(self):
        """Returns a wrapped saved or unsaved infant birth.
        """
        model_obj = self.karabo_subject_screening_obj or self.karabo_subject_screening_cls(
            subject_identifier=self.subject_identifier)
        return KaraboSubjectScreeningModelWrapper(model_obj=model_obj)

    infant_birth_cls = django_apps.get_model('td_infant.infantbirth')

    @property
    def infant_birth_obj(self):
        """Returns a infant birth model instance or None.
        """
        subject_identifier = self.subject_identifier + '-10'
        try:
            return self.infant_birth_cls.objects.get(
                subject_identifier=subject_identifier)
        except self.infant_birth_cls.DoesNotExist:
            return None

    @property
    def is_outside_schedule(self):
        subject_identifier = self.subject_identifier + '-10'
        latest_appointment = self.infant_appointment_cls.objects.filter(
            timepoint__gt=180,
            subject_identifier=subject_identifier).exclude(
                appt_status=NEW_APPT)
        return latest_appointment

