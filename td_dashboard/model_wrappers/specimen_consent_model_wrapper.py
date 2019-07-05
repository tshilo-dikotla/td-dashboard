from django.conf import settings

from edc_model_wrapper import ModelWrapper


class SpecimenConsentModelWrapper(ModelWrapper):

    model = 'td_maternal.specimenconsent'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'screening_listboard_url')
    next_url_attrs = ['screening_identifier']
    querystring_attrs = ['subject_identifier', 'screening_identifier']
