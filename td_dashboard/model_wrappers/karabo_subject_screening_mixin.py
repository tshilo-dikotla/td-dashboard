from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .karabo_screening_model_wrapper import KaraboSubjectScreeningModelWrapper


class KaraboScreeningModelWrapperMixin:

    karabo_screening_model_wrapper_cls = KaraboSubjectScreeningModelWrapper

    karabo_subject_screening_cls = django_apps.get_model(
        'td_maternal.karabosubjectscreening')

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
