from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .td_consent_version_model_wrapper import TDConsentVersionModelWrapper


class TDConsentVersionModelWrapperMixin:

    consent_version_model_wrapper_cls = TDConsentVersionModelWrapper

    @property
    def consent_version_model_obj(self):
        """Returns a TD Consent Version model instance or None.
         """
        try:
            print(">>>>>>>>>>>>>>>>>>>>>>>", self.consent_version_cls.objects.get(
                **self.consent_version_options).screening_identifier)
            return self.consent_version_cls.objects.get(
                **self.consent_version_options)
        except ObjectDoesNotExist:
            print("NOPE!!!", self.consent_version_options)
            return None

    @property
    def consent_version(self):
        """Returns a wrapped saved or unsaved consent version.
        """
        model_obj = self.consent_version_model_obj or self.consent_version_cls(
            **self.consent_version_options)
        return self.consent_version_model_wrapper_cls(model_obj=model_obj)

    @property
    def consent_version_cls(self):
        return django_apps.get_model('td_maternal.tdconsentversion')

    @property
    def consent_version_options(self):
        """Returns a dictionary of options to create a new
        unpersisted TD consent version model instance.
        """
        options = dict(
            screening_identifier=self.object.screening_identifier,
            version='3')
        return options
