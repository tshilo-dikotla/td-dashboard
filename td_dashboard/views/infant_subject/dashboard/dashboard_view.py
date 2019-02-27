from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.views.generic.base import ContextMixin
from edc_action_item.site_action_items import site_action_items
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.views import DashboardView as BaseDashboardView
from edc_navbar import NavbarViewMixin
from edc_registration.models import RegisteredSubject
from edc_subject_dashboard.view_mixins import SubjectDashboardViewMixin
from td_maternal.action_items import MATERNAL_LOCATOR_ACTION

from ....model_wrappers import (
    InfantAppointmentModelWrapper, InfantDummyConsentModelWrapper,
    InfantCrfModelWrapper, InfantRequisitionModelWrapper,
    InfantVisitModelWrapper, SubjectLocatorModelWrapper,
    InfantBirthModelWrapper, MaternalRegisteredSubjectModelWrapper)


class InfantBirthValues(object):

    infant_birth_cls = django_apps.get_model('td_infant.infantbirth')

    def __init__(self, subject_identifier=None):
        self.subject_identifier = subject_identifier

    @property
    def infant_birth_obj(self):
        """Returns a infant birth model instance or None.
        """
        try:
            return self.infant_birth_cls.objects.get(
                subject_identifier=self.subject_identifier)
        except ObjectDoesNotExist:
            return None

    @property
    def infant_birth(self):
        """Returns a wrapped saved or unsaved infant birth.
        """
        model_obj = self.infant_birth_obj or self.infant_birth_cls(
            subject_identifier=self.subject_identifier)
        return InfantBirthModelWrapper(model_obj=model_obj)


class InfantBirthButtonCls(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        infant_birth_values = InfantBirthValues(
            subject_identifier=self.subject_identifier)
        context.update(
            infant_birth_values=infant_birth_values,)
        return context


class MaternalRegisteredSubjectCls(ContextMixin):

    @property
    def maternal_registered_subject(self):
        subject_identifier = self.kwargs.get('subject_identifier')
        try:
            infant_registered_subject = RegisteredSubject.objects.get(
                subject_identifier=subject_identifier)
        except RegisteredSubject.DoesNotExist:
            raise ValidationError(
                "Registered subject for infant is expected to exist.")
        else:
            try:
                maternal_registered_subject = RegisteredSubject.objects.get(
                    subject_identifier=infant_registered_subject.relative_identifier)
            except RegisteredSubject.DoesNotExist:
                raise ValidationError(
                    "Registered subject for the monther is expected to exist.")
            else:
                return MaternalRegisteredSubjectModelWrapper(maternal_registered_subject)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            maternal_registered_subject=self.maternal_registered_subject)
        return context


class DashboardView(
        EdcBaseViewMixin, SubjectDashboardViewMixin,
        NavbarViewMixin, BaseDashboardView, InfantBirthButtonCls,
        MaternalRegisteredSubjectCls):

    dashboard_url = 'infant_subject_dashboard_url'
    dashboard_template = 'infant_subject_dashboard_template'
    appointment_model = 'td_infant.appointment'
    appointment_model_wrapper_cls = InfantAppointmentModelWrapper
    crf_model_wrapper_cls = InfantCrfModelWrapper
    requisition_model_wrapper_cls = InfantRequisitionModelWrapper
    consent_model = 'td_infant.infantdummysubjectconsent'
    consent_model_wrapper_cls = InfantDummyConsentModelWrapper
    navbar_name = 'td_dashboard'
    visit_attr = 'infantvisit'
    navbar_selected_item = 'infant_subject'
    visit_model_wrapper_cls = InfantVisitModelWrapper
    subject_locator_model = 'td_maternal.maternallocator'
    subject_locator_model_wrapper_cls = SubjectLocatorModelWrapper
    mother_infant_study = True
    infant_links = False
    maternal_links = True
    special_forms_include_value = "td_dashboard/infant_subject/dashboard/special_forms.html"
    maternal_dashboard_include_value = "td_dashboard/maternal_subject/dashboard/maternal_dashboard_links.html"

    def get_subject_locator_or_message(self):
        obj = None
        subject_identifier = self.kwargs.get('subject_identifier')
        try:
            obj = self.subject_locator_model_cls.objects.get(
                subject_identifier=subject_identifier)
        except ObjectDoesNotExist:
            action_cls = site_action_items.get(
                self.subject_locator_model_cls.action_name)
            action_item_model_cls = action_cls.action_item_model_cls()
            try:
                action_item_model_cls.objects.get(
                    subject_identifier=subject_identifier,
                    action_type__name=MATERNAL_LOCATOR_ACTION)
            except ObjectDoesNotExist:
                action_cls(
                    subject_identifier=subject_identifier)
        return obj