from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .maternal_death_report_model_wrapper import MaternalDeathReportModelWrapper


class MaternalDeathReportModelWrapperMixin:

    maternal_death_report_model_wrapper_cls = MaternalDeathReportModelWrapper

    @property
    def maternal_death_report_model_obj(self):
        """Returns a maternal death model instance or None.
        """
        try:
            return self.maternal_death_report_cls.objects.get(**self.maternal_death_report_options)
        except ObjectDoesNotExist:
            return None

    @property
    def maternal_death_report(self):
        """Returns a wrapped saved or unsaved maternal death report.
        """
        model_obj = self.maternal_death_report_model_obj or self.maternal_death_report_cls(
            **self.create_maternal_death_report_options)
        return self.maternal_death_report_model_wrapper_cls(model_obj=model_obj)

    @property
    def maternal_death_report_cls(self):
        return django_apps.get_model('td_prn.maternaldeathreport')

    @property
    def create_maternal_death_report_options(self):
        """Returns a dictionary of options to create a new
        unpersisted maternal death report model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def maternal_death_report_options(self):
        """Returns a dictionary of options to get an existing
        maternal death report model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options
