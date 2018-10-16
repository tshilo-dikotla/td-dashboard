from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings


class AppConfig(DjangoAppConfig):
    name = 'td_dashboard'
    admin_site_name = 'td_test_admin'
    include_in_administration_section = False


if settings.APP_NAME == 'td_dashboard':

    from edc_appointment.appointment_config import AppointmentConfig
    from edc_appointment.apps import AppConfig as BaseEdcAppointmentAppConfig

    class EdcAppointmentAppConfig(BaseEdcAppointmentAppConfig):
        configurations = [
            AppointmentConfig(
                model='td_dashboard.appointment',
                related_visit_model='td_dashboard.subjectvisit',
                appt_type='hospital')]
