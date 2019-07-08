from dateutil import relativedelta
from django.apps import apps as django_apps
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from edc_base.utils import get_utcnow
from edc_constants.constants import OFF_STUDY, DEAD, NEW

from edc_action_item.site_action_items import site_action_items
from edc_appointment.constants import NEW_APPT


class DashboardViewMixin:

    def get_onschedule_model_obj(self, schedule):
        try:
            return schedule.onschedule_model_cls.objects.get(
                subject_identifier=self.subject_identifier,
                schedule_name=schedule.name)
        except ObjectDoesNotExist:
            return None

    def get_death_or_message(self, visit_cls=None, death_cls=None,
                             death_report_action=None):
        obj = None
        subject_identifier = self.kwargs.get('subject_identifier')

        try:
            obj = visit_cls.objects.get(
                appointment__subject_identifier=subject_identifier,
                survival_status=DEAD)
        except ObjectDoesNotExist:
            self.delete_action_item_if_new(death_cls)
        else:
            if obj.survival_status == DEAD:
                self.action_cls_item_creator(
                    subject_identifier=subject_identifier,
                    action_cls=death_cls,
                    action_type=death_report_action)

    def get_offstudy_or_message(self, visit_cls=None, offstudy_cls=None,
                                offstudy_action=None):
        obj = None

        subject_identifier = self.kwargs.get('subject_identifier')
        try:
            obj = visit_cls.objects.get(
                appointment__subject_identifier=subject_identifier,
                study_status=OFF_STUDY)
        except ObjectDoesNotExist:
            self.delete_action_item_if_new(offstudy_cls)
        else:
            self.action_cls_item_creator(
                subject_identifier=subject_identifier,
                action_cls=offstudy_cls,
                action_type=offstudy_action)
        return obj

    def update_messages(self, offstudy_cls=None):

        if self.get_action_item_obj(offstudy_cls):
            form = offstudy_cls._meta.verbose_name
            msg = mark_safe(
                f'Please complete {form}, cannot add any new data.')
            messages.add_message(self.request, messages.ERROR, msg)

    def update_karabo_message(self):
        karabo_screening_cls = django_apps.get_model(
            'td_maternal.karabosubjectscreening')
        karabo_consent_cls = django_apps.get_model(
            'td_maternal.karabosubjectconsent')
        karabo_offstudy_cls = django_apps.get_model(
            'td_infant.karabooffstudy')

        subject_identifier = self.kwargs.get('subject_identifier')
        infant_identifier = subject_identifier

        if len(subject_identifier.split('-')) == 3:
            infant_identifier = subject_identifier + '-10'
        else:
            subject_identifier = subject_identifier[:-3]

        try:
            karabo_screening_obj = karabo_screening_cls.objects.get(
                subject_identifier=subject_identifier)
        except karabo_screening_cls.DoesNotExist:
            if (not self.offstudy_obj and not self.is_outside_schedule and
                    self.infant_age_valid):
                form = karabo_screening_cls._meta.verbose_name
                msg = mark_safe(
                    'Participant is eligible to partake in the Karabo study.'
                    f'Please complete {form}.')
                messages.add_message(self.request, messages.WARNING, msg)
        else:
            try:
                karabo_consent_cls.objects.get(
                    subject_identifier=subject_identifier)
            except karabo_consent_cls.DoesNotExist:
                if karabo_screening_obj.is_eligible:
                    form = karabo_consent_cls._meta.verbose_name
                    msg = mark_safe(
                        'Participant is eligible to partake in the Karabo study.'
                        f'Please complete {form}.')
                    messages.add_message(self.request, messages.WARNING, msg)
            else:
                try:
                    karabo_offstudy_cls.objects.get(
                        infant_visit__appointment__subject_identifier=infant_identifier)
                except karabo_offstudy_cls.DoesNotExist:
                    msg = mark_safe(
                        'Participant has been enrolled in the Karabo study.')
                    messages.add_message(self.request, messages.SUCCESS, msg)

    @property
    def offstudy_obj(self):
        subject_identifier = self.kwargs.get('subject_identifier')
        infant_identifier = subject_identifier

        if len(subject_identifier.split('-')) == 3:
            infant_identifier = subject_identifier + '-10'
        else:
            subject_identifier = subject_identifier[:-3]

        maternal_offstudy_cls = django_apps.get_model(
            'td_prn.maternaloffstudy')
        infant_offstudy_cls = django_apps.get_model(
            'td_prn.infantoffstudy')
        try:
            return maternal_offstudy_cls.objects.get(
                subject_identifier=subject_identifier)
        except maternal_offstudy_cls.DoesNotExist:
            try:
                return infant_offstudy_cls.objects.get(
                    subject_identifier=infant_identifier)
            except infant_offstudy_cls.DoesNotExist:
                return None

    @property
    def is_outside_schedule(self):
        subject_identifier = self.kwargs.get('subject_identifier')
        if len(subject_identifier.split('-')) == 3:
            subject_identifier = subject_identifier + '-10'

        infant_appointment_cls = django_apps.get_model(
            'td_infant.appointment')
        latest_appointment = infant_appointment_cls.objects.filter(
            timepoint__gt=180,
            subject_identifier=subject_identifier).exclude(
                appt_status=NEW_APPT)
        return latest_appointment

    @property
    def infant_age_valid(self):
        if self.maternal_labour_del():
            birth_datetime = self.maternal_labour_del().delivery_datetime
            difference = relativedelta.relativedelta(get_utcnow(), birth_datetime)
            months = 0
            if difference.years > 0:
                months = difference.years * 12
            return (months + difference.months) < 21
        return False

    def maternal_labour_del(self):
        maternal_labour_del_cls = django_apps.get_model(
            'td_maternal.maternallabourdel')
        subject_identifier = self.kwargs.get('subject_identifier')

        if len(subject_identifier.split('-')) != 3:
            subject_identifier = subject_identifier[:-3]

        try:
            maternal_labour_del = maternal_labour_del_cls.objects.get(
                subject_identifier=subject_identifier)
        except maternal_labour_del_cls.DoesNotExist:
            return None
        else:
            return maternal_labour_del

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

    def delete_action_item_if_new(self, action_model_cls):
        action_item_obj = self.get_action_item_obj(action_model_cls)
        if action_item_obj:
            action_item_obj.delete()

    def get_action_item_obj(self, model_cls):
        subject_identifier = self.kwargs.get('subject_identifier')
        action_cls = site_action_items.get(
            model_cls.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()

        try:
            action_item_obj = action_item_model_cls.objects.get(
                subject_identifier=subject_identifier,
                action_type__name=model_cls.action_name,
                status=NEW)
        except action_item_model_cls.DoesNotExist:
            return None
        return action_item_obj
