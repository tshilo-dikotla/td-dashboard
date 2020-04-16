from django.apps import apps as django_apps
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from edc_constants.constants import YES

from edc_subject_dashboard import SubjectVisitModelWrapper as BaseSubjectVisitModelWrapper


class MaternalVisitModelWrapper(BaseSubjectVisitModelWrapper):

    model = 'td_maternal.maternalvisit'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'subject_dashboard_url')
    next_url_attrs = ['subject_identifier', 'appointment', 'reason']

    @property
    def appointment(self):
        return str(self.object.appointment.id)
