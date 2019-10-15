from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .infant_death_report_model_wrapper import InfantDeathReportModelWrapper


class InfantDeathReportModelWrapperMixin:

    infant_death_report_model_wrapper_cls = InfantDeathReportModelWrapper

    @property
    def infant_death_report_model_obj(self):
        """Returns a infant death model instance or None.
        """
        try:
            return self.infant_death_report_cls.objects.get(**self.infant_death_report_options)
        except ObjectDoesNotExist:
            return None

    @property
    def infant_death_report(self):
        """Returns a wrapped saved or unsaved infant death report.
        """
        model_obj = self.infant_death_report_model_obj or self.infant_death_report_cls(
            **self.create_infant_death_report_options)
        return self.infant_death_report_model_wrapper_cls(model_obj=model_obj)

    @property
    def infant_death_report_cls(self):
        return django_apps.get_model('td_prn.infantdeathreport')

    @property
    def create_infant_death_report_options(self):
        """Returns a dictionary of options to create a new
        unpersisted infant death report model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def infant_death_report_options(self):
        """Returns a dictionary of options to get an existing
        infant death report model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options
