from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ValidationError
from edc_model_wrapper import ModelWrapper


class KaraboSubjectConsentModelWrapper(ModelWrapper):

    model = 'td_infant.karabosubjectconsent'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'infant_subject_dashboard_url')
    next_url_attrs = ['subject_identifier']
    querystring_attrs = ['screening_identifier', 'subject_identifier']

    @property
    def screening_identifier(self):
        """
        """
        model_cls = django_apps.get_model('td_infant.karabosubjectscreening')
        try:
            karabo_model_obj = model_cls.objects.get(
                subject_identifier=self.object.subject_identifier)
        except model_cls.DoesNotExist:
            raise ValidationError(
                f'Missing Karabo Screening.')
        else:
            return karabo_model_obj.screening_identifier
