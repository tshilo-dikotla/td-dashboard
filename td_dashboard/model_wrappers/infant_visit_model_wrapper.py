from django.conf import settings
from edc_subject_dashboard import SubjectVisitModelWrapper as BaseSubjectVisitModelWrapper


class InfantVisitModelWrapper(BaseSubjectVisitModelWrapper):

    model = 'td_infant.infantvisit'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'infant_subject_dashboard_url')
    next_url_attrs = ['subject_identifier', 'appointment', 'reason']

    @property
    def appointment(self):
        return str(self.object.appointment.id)
