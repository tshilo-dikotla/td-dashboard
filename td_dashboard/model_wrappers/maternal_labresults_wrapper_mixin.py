from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .maternal_labresults_model_wrapper import MaternalLabResultsModelWrapper


class MaternalLabResultsModelWrapperMixin:

    maternal_labresults_model_wrapper_cls = MaternalLabResultsModelWrapper

    @property
    def maternal_labresults_model_obj(self):
        """Returns a maternal lab results model instance or None.
        """
        try:
            return self.maternal_labresults_cls.objects.get(
                **self.maternal_labresults_options)
        except ObjectDoesNotExist:
            return None

    @property
    def maternal_labresults(self):
        """Returns a wrapped saved or unsaved maternal lab results.
        """
        model_obj = self.maternal_labresults_model_obj or self.maternal_labresults_cls(
            **self.create_maternal_labresults_options)
        return self.maternal_labresults_model_wrapper_cls(model_obj=model_obj)

    @property
    def maternal_labresults_cls(self):
        return django_apps.get_model('td_maternal.maternallabresultsfiles')

    @property
    def create_maternal_labresults_options(self):
        """Returns a dictionary of options to create a new
        unpersisted maternal lab results model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def maternal_labresults_options(self):
        """Returns a dictionary of options to get an existing
        maternal lab results model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options
