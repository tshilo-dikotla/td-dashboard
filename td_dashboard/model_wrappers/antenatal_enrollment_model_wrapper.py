from django.conf import settings

from edc_model_wrapper import ModelWrapper


class AntenatalEnrollmentModelWrapper(ModelWrapper):

    model = 'td_maternal.antenatalenrollment'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'subject_dashboard_url')
    next_url_attrs = ['subject_identifier', 'screening_identifier']
    querystring_attrs = ['subject_identifier']