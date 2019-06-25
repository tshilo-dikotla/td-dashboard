from django.apps import apps as django_apps
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.safestring import mark_safe
from django.views.generic.base import ContextMixin
from edc_base.view_mixins import EdcBaseViewMixin
from edc_constants.constants import OFF_STUDY, DEAD, NEW
from edc_dashboard.views import DashboardView as BaseDashboardView
from edc_navbar import NavbarViewMixin
from edc_registration.models import RegisteredSubject

from edc_action_item.site_action_items import site_action_items
from edc_subject_dashboard.view_mixins import SubjectDashboardViewMixin
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from td_prn.action_items import INFANTOFF_STUDY_ACTION
from td_prn.action_items import INFANT_DEATH_REPORT_ACTION

from ....model_wrappers import (
    InfantAppointmentModelWrapper, InfantDummyConsentModelWrapper,
    InfantCrfModelWrapper, InfantRequisitionModelWrapper, InfantOffstudyModelWrapper,
    InfantVisitModelWrapper, SubjectLocatorModelWrapper, ActionItemModelWrapper,
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
        self.update_messages()
        self.get_death_or_message()
        self.get_infant_offstudy_or_message()
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

    def get_death_or_message(self):
        obj = None
        infant_visit_cls = django_apps.get_model(
            'td_infant.infantvisit')
        infant_death_cls = django_apps.get_model(
            'td_prn.infantdeathreport')
        subject_identifier = self.kwargs.get('subject_identifier')

        try:
            obj = infant_visit_cls.objects.get(
                appointment__subject_identifier=subject_identifier,
                survival_status=DEAD)
        except ObjectDoesNotExist:
            self.delete_action_item_if_new(infant_death_cls)
        else:
            if obj.survival_status == DEAD:
                self.action_cls_item_creator(
                    subject_identifier=subject_identifier,
                    action_cls=infant_death_cls,
                    action_type=INFANT_DEATH_REPORT_ACTION)

    def get_infant_offstudy_or_message(self):
        obj = None
        infant_visit_cls = django_apps.get_model(
            'td_infant.infantvisit')
        infant_offstudy_cls = django_apps.get_model(
            'td_prn.infantoffstudy')
        subject_identifier = self.kwargs.get('subject_identifier')
        try:
            obj = infant_visit_cls.objects.get(
                appointment__subject_identifier=subject_identifier,
                study_status=OFF_STUDY)
        except ObjectDoesNotExist:
            self.delete_action_item_if_new(infant_offstudy_cls)
        else:
            self.action_cls_item_creator(
                subject_identifier=subject_identifier,
                action_cls=infant_offstudy_cls,
                action_type=INFANTOFF_STUDY_ACTION)
        return obj

    def action_cls_item_creator(
            self, subject_identifier=None, action_cls=None, action_type=None):
        action_cls = site_action_items.get(
            action_cls.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()
        try:
            action_item_model_cls.objects.get(
                subject_identifier=subject_identifier,
                action_type__name=action_type)
        except ObjectDoesNotExist:
            action_cls(
                subject_identifier=subject_identifier)

    def get_action_item_obj(self, model_cls):
        subject_identifier = self.kwargs.get('subject_identifier')
        action_cls = site_action_items.get(model_cls.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()

        try:
            action_item_obj = action_item_model_cls.objects.get(
                subject_identifier=subject_identifier,
                action_type__name=model_cls.action_name,
                status=NEW)
        except action_item_model_cls.DoesNotExist:
            return None
        return action_item_obj

    def delete_action_item_if_new(self, action_model_cls):
        action_item_obj = self.get_action_item_obj(action_model_cls)
        if action_item_obj:
            action_item_obj.delete()

    def update_messages(self):
        infant_offstudy_cls = django_apps.get_model(
            'td_prn.infantoffstudy')

        if self.get_action_item_obj(infant_offstudy_cls):
            form = infant_offstudy_cls._meta.verbose_name
            msg = mark_safe(
                f'Please complete {form}, cannot add any new data.')
            messages.add_message(self.request, messages.ERROR, msg)
