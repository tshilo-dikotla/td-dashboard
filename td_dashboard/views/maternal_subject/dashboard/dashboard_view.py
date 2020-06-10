from td_maternal.action_items import MATERNAL_LOCATOR_ACTION
from td_maternal.helper_classes import MaternalStatusHelper
from td_prn.action_items import MATERNALOFF_STUDY_ACTION
from td_prn.action_items import MATERNAL_DEATH_REPORT_ACTION

from django.apps import apps as django_apps
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from edc_base.utils import get_utcnow
from edc_base.view_mixins import EdcBaseViewMixin
from edc_constants.constants import YES
from edc_navbar import NavbarViewMixin
from edc_registration.models import RegisteredSubject

from edc_action_item.site_action_items import site_action_items
from edc_appointment.constants import NEW_APPT
from edc_dashboard.views import DashboardView as BaseDashboardView
from edc_subject_dashboard.view_mixins import SubjectDashboardViewMixin

from ....model_wrappers import (
    AppointmentModelWrapper, SubjectConsentModelWrapper,
    MaternalVisitModelWrapper, SubjectLocatorModelWrapper,
    MaternalCrfModelWrapper, MaternalRequisitionModelWrapper,
    SubjectScreeningModelWrapper)
from ...view_mixin import DashboardViewMixin


class DashboardView(
        DashboardViewMixin, EdcBaseViewMixin, SubjectDashboardViewMixin,
        NavbarViewMixin, BaseDashboardView):

    dashboard_url = 'subject_dashboard_url'
    dashboard_template = 'subject_dashboard_template'
    appointment_model = 'edc_appointment.appointment'
    appointment_model_wrapper_cls = AppointmentModelWrapper
    crf_model_wrapper_cls = MaternalCrfModelWrapper
    requisition_model_wrapper_cls = MaternalRequisitionModelWrapper
    consent_model = 'td_maternal.subjectconsent'
    consent_model_wrapper_cls = SubjectConsentModelWrapper
    navbar_name = 'td_dashboard'
    visit_attr = 'maternalvisit'
    navbar_selected_item = 'consented_subject'
    subject_locator_model = 'td_maternal.maternallocator'
    subject_locator_model_wrapper_cls = SubjectLocatorModelWrapper
    visit_model_wrapper_cls = MaternalVisitModelWrapper
    special_forms_include_value = "td_dashboard/maternal_subject/dashboard/special_forms.html"
    mother_infant_study = True
    infant_links = True
    maternal_links = False
    infant_dashboard_include_value = "td_dashboard/maternal_subject/dashboard/infant_dashboard_links.html"
    infant_subject_dashboard_url = 'infant_subject_dashboard_url'
    data_action_item_template = "td_dashboard/maternal_subject/dashboard/data_manager.html"

    @property
    def subject_screening(self):
        """Return a wrapped subject screening obj.
        """
        subject_screening_cls = django_apps.get_model(
            'td_maternal.subjectscreening')
        try:
            subject_screening = subject_screening_cls.objects.get(
                subject_identifier=self.subject_identifier)
        except subject_screening_cls.DoesNotExist:
            raise ValidationError('Subject Screening must exist.')
        else:
            return SubjectScreeningModelWrapper(subject_screening)

    @property
    def infant_registered_subject(self):
        """Returns an infant registered subject.
        """
        subject_identifier = self.kwargs.get('subject_identifier')
        try:
            registered_subject = RegisteredSubject.objects.get(
                relative_identifier=subject_identifier)
        except RegisteredSubject.DoesNotExist:
            return None
        else:
            return registered_subject

    @property
    def enrollment_hiv_status(self):
        """Returns mother's current hiv status.
        """
        subject_identifier = self.kwargs.get('subject_identifier')

        antenatal_enrollment_cls = django_apps.get_model(
            'td_maternal.antenatalenrollment')
        try:
            antenatal_enrollment = antenatal_enrollment_cls.objects.get(
                subject_identifier=subject_identifier)
        except antenatal_enrollment_cls.DoesNotExist:
            return None
        else:
            return antenatal_enrollment.enrollment_hiv_status

    @property
    def hiv_status(self):
        """Returns mother's current hiv status.
        """
        maternal_visit_cls = django_apps.get_model(
            MaternalVisitModelWrapper.model)
        subject_identifier = self.kwargs.get('subject_identifier')
        latest_visit = maternal_visit_cls.objects.filter(
            subject_identifier=subject_identifier,).order_by(
            '-report_datetime').first()

        if latest_visit:
            maternal_status_helper = MaternalStatusHelper(latest_visit)
            return maternal_status_helper.hiv_status
        else:
            return self.enrollment_hiv_status

    @property
    def rando_status(self):
        """Returns mother's current randomization status.
        """
        maternal_rando_cls = django_apps.get_model(
            'td_maternal.maternalrando')
        subject_identifier = self.kwargs.get('subject_identifier')
        try:
            rando_status = maternal_rando_cls.objects.get(
                maternal_visit__subject_identifier=subject_identifier)
        except maternal_rando_cls.DoesNotExist:
            return None
        else:
            return rando_status.rx

    @property
    def maternal_ga(self):
        """Returns mother's current hiv status.
        """
        maternal_lab_del = self.is_maternal_labour_del()

        maternal_ultrasound_cls = django_apps.get_model(
            'td_maternal.maternalultrasoundinitial')
        subject_identifier = self.kwargs.get('subject_identifier')
        try:
            maternal_ultrasound = maternal_ultrasound_cls.objects.get(
                maternal_visit__subject_identifier=subject_identifier)
        except maternal_ultrasound_cls.DoesNotExist:
            return None
        else:
            if not maternal_lab_del:
                return int(abs(
                    40 - ((maternal_ultrasound.edd_confirmed - get_utcnow().date()).days / 7)))
            else:
                return int(abs(
                    40 - ((maternal_ultrasound.edd_confirmed - maternal_lab_del.report_datetime.date()).days / 7)))

    def is_maternal_labour_del(self):
        maternal_labour_del_cls = django_apps.get_model(
            'td_maternal.maternallabourdel')
        subject_identifier = self.kwargs.get('subject_identifier')
        try:
            maternal_labour_del = maternal_labour_del_cls.objects.get(
                subject_identifier=subject_identifier)
        except maternal_labour_del_cls.DoesNotExist:
            return None
        else:
            return maternal_labour_del

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        maternal_offstudy_cls = django_apps.get_model('td_prn.maternaloffstudy')
        maternal_visit_cls = django_apps.get_model('td_maternal.maternalvisit')
        maternal_death_cls = django_apps.get_model('td_prn.maternaldeathreport')

        self.update_messages(offstudy_cls=maternal_offstudy_cls)
        self.update_karabo_message()
        self.get_death_or_message(visit_cls=maternal_visit_cls,
                                  death_cls=maternal_death_cls,
                                  death_report_action=MATERNAL_DEATH_REPORT_ACTION)
        self.get_offstudy_or_message(visit_cls=maternal_visit_cls,
                                     offstudy_cls=maternal_offstudy_cls,
                                     offstudy_action=MATERNALOFF_STUDY_ACTION)
        context.update(subject_screening=self.subject_screening,
                       hiv_status=self.hiv_status,
                       enrollment_hiv_status=self.enrollment_hiv_status,
                       rando_status=self.rando_status,
                       maternal_ga=self.maternal_ga,
                       open_action_items=self.open_action_items)
        self.get_covid_object_or_message()
        context = self.add_url_to_context(
            new_key='dashboard_url_name',
            existing_key=self.dashboard_url,
            context=context)

        return context

    def set_current_schedule(self, onschedule_model_obj=None,
                             schedule=None, visit_schedule=None,
                             is_onschedule=True):
        if onschedule_model_obj:
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

    def get_covid_object_or_message(self):
        subject_identifier = self.kwargs.get('subject_identifier')
        maternal_visit_cls = django_apps.get_model('td_maternal.maternalvisit')
        maternal_covid_screening_cls = django_apps.get_model(
            'td_maternal.maternalcovidscreening')

        maternal_visits = maternal_visit_cls.objects.filter(
            appointment__subject_identifier=subject_identifier)

        for visit in maternal_visits:
            try:
                maternal_covid_screening_cls.objects.get(
                    maternal_visit=visit)
            except maternal_covid_screening_cls.DoesNotExist:
                form = maternal_covid_screening_cls._meta.verbose_name
                msg = mark_safe(
                    f'Please complete {form} for visit {visit.visit_code} as '
                    'it is indicated as a covid visit.')
                messages.add_message(self.request, messages.WARNING, msg)
