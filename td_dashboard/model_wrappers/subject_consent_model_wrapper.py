from django.conf import settings
from edc_model_wrapper import ModelWrapper

from .td_consent_version_model_wrapper_mixin import TDConsentVersionModelWrapperMixin


class SubjectConsentModelWrapper(TDConsentVersionModelWrapperMixin,
                                 ModelWrapper):

    model = 'td_maternal.subjectconsent'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'screening_listboard_url')
    next_url_attrs = ['screening_identifier']
    querystring_attrs = ['screening_identifier', 'subject_identifier']
