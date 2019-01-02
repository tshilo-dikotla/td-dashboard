from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.base import ContextMixin

from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.views import DashboardView as BaseDashboardView
from edc_navbar import NavbarViewMixin
from edc_registration.models import RegisteredSubject
from edc_subject_dashboard.view_mixins import SubjectDashboardViewMixin

from ....model_wrappers import (
    AppointmentModelWrapper, SubjectConsentModelWrapper,
    InfantCrfModelWrapper, InfantRequisitionModelWrapper,
    InfantVisitModelWrapper, SubjectLocatorModelWrapper,
    InfantBirthModelWrapper)


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
        infant_birth_values = InfantBirthValues(subject_identifier=self.subject_identifier)
        context.update(
            infant_birth_values=infant_birth_values,)
        return context


class DashboardView(
        EdcBaseViewMixin, SubjectDashboardViewMixin,
        NavbarViewMixin, BaseDashboardView, InfantBirthButtonCls):

    dashboard_url = 'infant_subject_dashboard_url'
    dashboard_template = 'infant_subject_dashboard_template'
    appointment_model = 'edc_appointment.appointment'
    appointment_model_wrapper_cls = AppointmentModelWrapper
    crf_model_wrapper_cls = InfantCrfModelWrapper
    requisition_model_wrapper_cls = InfantRequisitionModelWrapper
    consent_model = 'td_maternal.subjectconsent'
    consent_model_wrapper_cls = SubjectConsentModelWrapper
    navbar_name = 'td_dashboard'
    visit_attr = 'infantvisit'
    navbar_selected_item = 'infant_subject'
    visit_model_wrapper_cls = InfantVisitModelWrapper
    subject_locator_model = 'edc_locator.subjectlocator'
    subject_locator_model_wrapper_cls = SubjectLocatorModelWrapper
    special_forms_include_value = "td_dashboard/infant_subject/dashboard/special_forms.html"
