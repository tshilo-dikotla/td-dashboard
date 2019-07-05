from django.conf import settings
from edc_visit_schedule.model_wrappers import (
    CrfModelWrapper as BaseCrfModelWrapper)


class InfantCrfModelWrapper(BaseCrfModelWrapper):

    visit_model_attr = 'infant_visit'

    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'infant_subject_dashboard_url')
    next_url_attrs = ['appointment', 'subject_identifier']
    querystring_attrs = [visit_model_attr]

    @property
    def infant_visit(self):
        return str(getattr(self.object, self.visit_model_attr).id)

    @property
    def appointment(self):
        return str(getattr(self.object, self.visit_model_attr).appointment.id)

    @property
    def subject_identifier(self):
        return getattr(self.object, self.visit_model_attr).subject_identifier
