from django.conf import settings
from edc_model_wrapper import ModelWrapper


class TDConsentVersionModelWrapper(ModelWrapper):

    model = 'td_maternal.tdconsentversion'
    visit_model_attr = 'maternal_visit'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'screening_listboard_url')
    next_url_attrs = ['screening_identifier']
    querystring_attrs = ['screening_identifier', visit_model_attr]
