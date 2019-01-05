from django.conf import settings

from edc_model_wrapper import ModelWrapper


class InfantDummyConsentModelWrapper(ModelWrapper):

    model = 'td_infant.infantdummysubjectconsent'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'infant_listboard_url')
    next_url_attrs = ['subject_identifier']
    querystring_attrs = ['subject_identifier']
