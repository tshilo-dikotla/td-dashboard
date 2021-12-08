from django.conf import settings

from edc_model_wrapper import ModelWrapper


class MaternalClinicianNotesModelWrapper(ModelWrapper):

    model = 'td_maternal.cliniciannotesarchives'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'subject_dashboard_url')
    next_url_attrs = ['subject_identifier']
    querystring_attrs = ['subject_identifier', ]
