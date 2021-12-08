from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .infant_labresults_model_wrapper import InfantLabResultsModelWrapper


class InfantLabResultsModelWrapperMixin:

    infant_labresults_model_wrapper_cls = InfantLabResultsModelWrapper

    @property
    def infant_labresults_model_obj(self):
        """Returns a infant lab results model instance or None.
        """
        try:
            return self.infant_labresults_cls.objects.get(
                **self.infant_labresults_options)
        except ObjectDoesNotExist:
            return None

    @property
    def infant_labresults(self):
        """Returns a wrapped saved or unsaved infant lab results.
        """
        model_obj = self.infant_labresults_model_obj or self.infant_labresults_cls(
            **self.create_infant_labresults_options)
        return self.infant_labresults_model_wrapper_cls(model_obj=model_obj)

    @property
    def infant_labresults_cls(self):
        return django_apps.get_model('td_infant.infantlabresultsfiles')

    @property
    def create_infant_labresults_options(self):
        """Returns a dictionary of options to create a new
        unpersisted infant lab results model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def infant_labresults_options(self):
        """Returns a dictionary of options to get an existing
        infant lab results model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options
