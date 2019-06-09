from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .karabo_subject_consent_model_wrapper import KaraboSubjectConsentModelWrapper


class KaraboSubjectConsentModelWrapperMixin:

    karabo_consent_model_wrapper_cls = KaraboSubjectConsentModelWrapper

    karabo_subject_consent_cls = django_apps.get_model(
        'td_maternal.karabosubjectconsent')

    infant_appointment_cls = django_apps.get_model(
        'td_infant.appointment')

    @property
    def is_karabo_eligible(self):
        if self.karabo_subject_screening_obj:
            return self.karabo_subject_screening_obj.is_eligible
        return None

    @property
    def karabo_subject_consent_obj(self):
        """Returns a karabo subject consent model instance or None.
        """
        try:
            return self.karabo_subject_consent_cls.objects.get(
                subject_identifier=self.subject_identifier)
        except ObjectDoesNotExist:
            return None

    @property
    def karabo_subject_consent(self):
        """Returns a wrapped saved or unsaved infant birth.
        """
        model_obj = self.karabo_subject_consent_obj or self.karabo_subject_consent_cls(
            subject_identifier=self.subject_identifier)
        return KaraboSubjectConsentModelWrapper(model_obj=model_obj)
