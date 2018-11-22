from django.conf import settings
from edc_subject_dashboard import SubjectVisitModelWrapper as BaseSubjectVisitModelWrapper


class MaternalVisitModelWrapper(BaseSubjectVisitModelWrapper):

    model = 'td_maternal.maternalvisit'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'subject_dashboard_url')
