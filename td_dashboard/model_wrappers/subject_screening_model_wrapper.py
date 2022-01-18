from dateutil import relativedelta
from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from edc_base.utils import get_utcnow
from edc_model_wrapper import ModelWrapper

from edc_consent import ConsentModelWrapperMixin
from edc_consent.site_consents import site_consents
from td_prn.action_items import MATERNALOFF_STUDY_ACTION

from .antenantal_visit_membership_wrapper_mixin import AntenatalVisitMembershipWrapperMixin
from .antenatal_enrollment_wrapper_mixin import AntenatalEnrollmentModelWrapperMixin
from .karabo_subject_consent_mixin import KaraboSubjectConsentModelWrapperMixin
from .karabo_subject_screening_mixin import KaraboScreeningModelWrapperMixin
from .maternal_contact_model_wrapper_mixin import MaternalContactModelWrapperMixin
from .maternal_death_report_wrapper_mixin import MaternalDeathReportModelWrapperMixin
from .maternal_labour_del_wrapper_mixin import MaternalLabourDelModelWrapperMixin
from .maternal_locator_wrapper_mixin import MaternalLocatorModelWrapperMixin
from .maternal_offstudy_wrapper_mixin import MaternalOffstudyModelWrapperMixin
from .specimen_consent_model_wrapper_mixin import SpecimenConsentModelWrapperMixin
from .subject_consent_model_wrapper import SubjectConsentModelWrapper
from .td_consent_version_model_wrapper_mixin import TDConsentVersionModelWrapperMixin


class SubjectScreeningModelWrapper(
        MaternalLabourDelModelWrapperMixin,
        AntenatalVisitMembershipWrapperMixin,
        AntenatalEnrollmentModelWrapperMixin,
        ConsentModelWrapperMixin,
        KaraboSubjectConsentModelWrapperMixin,
        KaraboScreeningModelWrapperMixin,
        MaternalLocatorModelWrapperMixin,
        MaternalOffstudyModelWrapperMixin,
        SpecimenConsentModelWrapperMixin,
        TDConsentVersionModelWrapperMixin,
        MaternalContactModelWrapperMixin,
        MaternalDeathReportModelWrapperMixin,
        ModelWrapper):

    consent_model_wrapper_cls = SubjectConsentModelWrapper
    model = 'td_maternal.subjectscreening'
    next_url_attrs = ['screening_identifier', 'subject_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'screening_listboard_url')

    @property
    def consent_object(self):
        """Returns a consent configuration object from site_consents
        relative to the wrapper's "object" report_datetime.
        """
        default_consent_group = django_apps.get_app_config(
            'edc_consent').default_consent_group
        consent_object = site_consents.get_consent_for_period(
            model=self.consent_model_wrapper_cls.model,
            report_datetime=self.consent_version_model_obj.report_datetime,
            consent_group=default_consent_group,
            version=self.consent_version or None)

        return consent_object

    @property
    def consented(self):
        return self.object.subject_identifier

    @property
    def subject_identifier(self):
        return self.object.subject_identifier

    @property
    def create_consent_options(self):
        options = super().create_consent_options
        options.update(screening_identifier=self.object.screening_identifier)
        return options

    @property
    def consent_model_obj(self):
        consent_model_cls = django_apps.get_model(
            self.consent_model_wrapper_cls.model)
        try:
            return consent_model_cls.objects.get(**self.consent_options)
        except ObjectDoesNotExist:
            return None

    @property
    def consent_version(self):
        consent_version_cls = django_apps.get_model(
            'td_maternal.tdconsentversion')
        try:
            consent_version_obj = consent_version_cls.objects.get(
                screening_identifier=self.object.screening_identifier)
        except consent_version_cls.DoesNotExist:
            return None
        return consent_version_obj.version

    @property
    def offstudy_obj(self):
        maternal_offstudy_cls = django_apps.get_model(
            'td_prn.maternaloffstudy')
        infant_offstudy_cls = django_apps.get_model(
            'td_prn.infantoffstudy')
        try:
            return maternal_offstudy_cls.objects.get(
                subject_identifier=self.object.subject_identifier)
        except maternal_offstudy_cls.DoesNotExist:
            try:
                return infant_offstudy_cls.objects.get(
                    subject_identifier=self.object.subject_identifier + '-10')
            except infant_offstudy_cls.DoesNotExist:
                return None

    @property
    def death_obj(self):
        maternal_death_cls = django_apps.get_model(
            'td_prn.maternaldeathreport')
        infant_death_cls = django_apps.get_model(
            'td_prn.infantdeathreport')
        try:
            return maternal_death_cls.objects.get(
                subject_identifier=self.object.subject_identifier)
        except maternal_death_cls.DoesNotExist:
            try:
                return infant_death_cls.objects.get(
                    subject_identifier=self.object.subject_identifier + '-10')
            except infant_death_cls.DoesNotExist:
                return None

    @property
    def infant_age_valid(self):
        if self.maternal_labour_del_model_obj:
            birth_datetime = self.maternal_labour_del_model_obj.delivery_datetime
            difference = relativedelta.relativedelta(
                get_utcnow(), birth_datetime)
            months = 0
            if difference.years > 0:
                months = difference.years * 12
            return (months + difference.months) < 21
        return False
