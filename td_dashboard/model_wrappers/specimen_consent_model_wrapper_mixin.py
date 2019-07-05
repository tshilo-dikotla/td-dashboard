from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .specimen_consent_model_wrapper import SpecimenConsentModelWrapper


class SpecimenConsentModelWrapperMixin:

    specimen_consent_model_wrapper_cls = SpecimenConsentModelWrapper

    @property
    def specimen_consent_obj(self):
        """Returns a specimen consent model instance or None.
        """
        try:
            return self.specimen_consent_cls.objects.get(**self.specimen_consent_options)
        except ObjectDoesNotExist:
            return None

    @property
    def specimen_consent(self):
        """Returns a wrapped saved or unsaved specimen consent.
        """
        model_obj = self.specimen_consent_obj or self.specimen_consent_cls(
            **self.create_specimen_consent_options)
        return self.specimen_consent_model_wrapper_cls(model_obj=model_obj)

    @property
    def specimen_consent_cls(self):
        return django_apps.get_model('td_maternal.specimenconsent')

    @property
    def create_specimen_consent_options(self):
        """Returns a dictionary of options to create a new
        unpersisted specimen consent model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def specimen_consent_options(self):
        """Returns a dictionary of options to get an existing
        specimen consent model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options
