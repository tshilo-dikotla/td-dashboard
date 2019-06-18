from dateutil import relativedelta
from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from edc_base.utils import get_utcnow
from edc_model_wrapper import ModelWrapper

from edc_consent import ConsentModelWrapperMixin
from td_prn.action_items import MATERNALOFF_STUDY_ACTION

from .antenantal_visit_membership_wrapper_mixin import AntenatalVisitMembershipWrapperMixin
from .antenatal_enrollment_wrapper_mixin import AntenatalEnrollmentModelWrapperMixin
from .karabo_subject_consent_mixin import KaraboSubjectConsentModelWrapperMixin
from .karabo_subject_screening_mixin import KaraboScreeningModelWrapperMixin
from .maternal_contact_model_wrapper_mixin import MaternalContactModelWrapperMixin
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
        ModelWrapper):

    consent_model_wrapper_cls = SubjectConsentModelWrapper
    model = 'td_maternal.subjectscreening'
    next_url_attrs = ['screening_identifier', 'subject_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'screening_listboard_url')

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
    def infant_age(self):
        if self.maternal_labour_del_model_obj:
            birth_datetime = self.maternal_labour_del_model_obj.delivery_datetime
            difference = relativedelta.relativedelta(get_utcnow(), birth_datetime)
            return difference.months
        return None
