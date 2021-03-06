from django.apps import apps as django_apps
from django.conf import settings
from edc_model_wrapper import ModelWrapper


class KaraboSubjectConsentModelWrapper(ModelWrapper):

    model = 'td_maternal.karabosubjectconsent'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'subject_dashboard_url')
    next_url_attrs = ['subject_identifier']
    querystring_attrs = ['screening_identifier', 'subject_identifier']

    @property
    def screening_identifier(self):
        """
        """
        model_cls = django_apps.get_model('td_maternal.karabosubjectscreening')
        try:
            karabo_model_obj = model_cls.objects.get(
                subject_identifier=self.object.subject_identifier)
        except model_cls.DoesNotExist:
            return None
        else:
            return karabo_model_obj.screening_identifier
