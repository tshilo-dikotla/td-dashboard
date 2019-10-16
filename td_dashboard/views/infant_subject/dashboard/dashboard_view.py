from dateutil import relativedelta
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.views.generic.base import ContextMixin
from edc_action_item.site_action_items import site_action_items
from edc_base.utils import get_utcnow
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.views import DashboardView as BaseDashboardView
from edc_registration.models import RegisteredSubject
from edc_subject_dashboard.view_mixins import SubjectDashboardViewMixin

from edc_navbar import NavbarViewMixin
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from td_dashboard.model_wrappers.infant_death_report_model_wrapper import InfantDeathReportModelWrapper
from td_prn.action_items import INFANTOFF_STUDY_ACTION
from td_prn.action_items import INFANT_DEATH_REPORT_ACTION

from ....model_wrappers import (
    InfantAppointmentModelWrapper, InfantDummyConsentModelWrapper,
    InfantCrfModelWrapper, InfantRequisitionModelWrapper, InfantOffstudyModelWrapper,
    InfantVisitModelWrapper, SubjectLocatorModelWrapper, ActionItemModelWrapper,
    InfantBirthModelWrapper, MaternalRegisteredSubjectModelWrapper)
from ...view_mixin import DashboardViewMixin


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

    @property
    def infant_offstudy_cls(self):
        return django_apps.get_model('td_prn.infantoffstudy')

    @property
    def infant_offstudy_model_obj(self):
        """Returns a infant offstudy model instance or None.
        """
        try:
            return self.infant_offstudy_cls.objects.get(**self.infant_offstudy_options)
        except ObjectDoesNotExist:
            return None

    @property
    def infant_offstudy(self):
        """Returns a wrapped saved or unsaved infant offstudy.
        """
        model_obj = self.infant_offstudy_model_obj or self.infant_offstudy_cls(
            **self.infant_offstudy_options)
        return InfantOffstudyModelWrapper(model_obj=model_obj)

    @property
    def infant_offstudy_options(self):
        """Returns a dictionary of options to get an existing
        infant offstudy model instance.
        """
        options = dict(
            subject_identifier=self.subject_identifier)
        return options

    @property
    def infant_death_report_cls(self):
        return django_apps.get_model('td_prn.infantdeathreport')

    @property
    def infant_death_report_model_obj(self):
        """Returns a infant death report model instance or None.
        """
        try:
            return self.infant_death_report_cls.objects.get(**self.infant_offstudy_options)
        except ObjectDoesNotExist:
            return None

    @property
    def infant_death_report(self):
        """Returns a wrapped saved or unsaved infant death report.
        """
        model_obj = self.infant_death_report_model_obj or self.infant_death_report_cls(
            **self.infant_offstudy_options)
        return InfantDeathReportModelWrapper(model_obj=model_obj)

    @property
    def infant_age(self):
        if self.infant_birth_obj:
            birth_date = self.infant_birth_obj.dob
            difference = relativedelta.relativedelta(
                get_utcnow().date(), birth_date)
            months = 0
            if difference.years > 0:
                months = difference.years * 12
            return months + difference.months
        return None


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
        DashboardViewMixin, EdcBaseViewMixin, SubjectDashboardViewMixin,
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
    action_item_model_wrapper_cls = ActionItemModelWrapper
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        infant_offstudy_cls = django_apps.get_model('td_prn.infantoffstudy')
        infant_visit_cls = django_apps.get_model('td_infant.infantvisit')
        infant_death_cls = django_apps.get_model('td_prn.infantdeathreport')

        self.update_messages(offstudy_cls=infant_offstudy_cls)
        self.get_death_or_message(visit_cls=infant_visit_cls,
                                  death_cls=infant_death_cls,
                                  death_report_action=INFANT_DEATH_REPORT_ACTION)
        self.get_offstudy_or_message(visit_cls=infant_visit_cls,
                                     offstudy_cls=infant_offstudy_cls,
                                     offstudy_action=INFANTOFF_STUDY_ACTION)
        self.update_karabo_message()
        context = self.add_url_to_context(
            new_key='dashboard_url_name',
            existing_key=self.dashboard_url,
            context=context)

        return context

    def set_current_schedule(self, onschedule_model_obj=None,
                             schedule=None, visit_schedule=None,
                             is_onschedule=True):
        if onschedule_model_obj and is_onschedule:
            self.current_schedule = schedule
            self.current_visit_schedule = visit_schedule
            self.current_onschedule_model = onschedule_model_obj
            self.onschedule_models.append(onschedule_model_obj)
            self.visit_schedules.update(
                {visit_schedule.name: visit_schedule})

    def get_onschedule_model_obj(self, schedule):
        try:
            return schedule.onschedule_model_cls.objects.get(
                subject_identifier=self.subject_identifier,
                schedule_name=schedule.name)
        except ObjectDoesNotExist:
            return None

    def get_subject_locator_or_message(self):
        """
        Overridden to stop system from generating subject locator
        action items for infant.
        """
        pass
