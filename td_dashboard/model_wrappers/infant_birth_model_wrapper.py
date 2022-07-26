from dateutil import relativedelta
from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from edc_base.utils import get_utcnow
from edc_model_wrapper import ModelWrapper

from edc_odk.model_wrappers import NoteToFileModelWrapperMixin
from edc_odk.model_wrappers import ClinicianNotesModelWrapperMixin
from edc_odk.model_wrappers import LabResultsModelWrapperMixin


class InfantBirthModelWrapper(NoteToFileModelWrapperMixin,
                              ClinicianNotesModelWrapperMixin,
                              LabResultsModelWrapperMixin,
                              ModelWrapper):

    model = 'td_infant.infantbirth'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'infant_subject_dashboard_url')
    next_url_attrs = ['subject_identifier']
    querystring_attrs = ['subject_identifier']

    @property
    def infant_birth_cls(self):
        return django_apps.get_model('td_infant.infantbirth')

    @property
    def infant_birth_obj(self):
        """Returns a infant birth model instance or None.
        """
        try:
            return self.infant_birth_cls.objects.get(
                subject_identifier=self.object.subject_identifier)
        except ObjectDoesNotExist:
            return None

    @property
    def infant_age(self):
        if self.infant_birth_obj:
            birth_date = self.infant_birth_obj.dob
            difference = relativedelta.relativedelta(
                get_utcnow().date(), birth_date)
            months = 0
            if difference.years > 0:
                months = difference.years * 12
            return months + difference.months
        return None
