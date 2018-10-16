from django.conf import settings

from edc_model_wrapper import ModelWrapper


class MaternalConsentModelWrapper(ModelWrapper):

    model = 'td_maternal.maternalconsent'
    next_url_name = settings.DASHBOARD_URL_NAMES.get('subject_dashboard_url')
    next_url_attrs = ['subject_identifier']
    querystring_attrs = [
        'eligibility_id', 'gender', 'first_name', 'initials', 'modified']
