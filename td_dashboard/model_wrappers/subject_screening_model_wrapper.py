from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from edc_consent import ConsentModelWrapperMixin
from edc_model_wrapper import ModelWrapper

from .maternal_consent_model_wrapper import MaternalConsentModelWrapper


class SubjectScreeningModelWrapper(ConsentModelWrapperMixin, ModelWrapper):

    consent_model_wrapper_cls = MaternalConsentModelWrapper
    model = 'td_maternal.subjectscreening'
    next_url_attrs = ['screening_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'subject_screening_listboard_url')

    @property
    def consented(self):
        return 'iii'

    @property
    def consent_model_obj(self):
        consent_model_cls = django_apps.get_model(
            self.consent_model_wrapper_cls.model)
        try:
            return consent_model_cls.objects.get(**self.consent_options)
        except ObjectDoesNotExist:
            return None