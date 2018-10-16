from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.views import DashboardView as BaseDashboardView
from edc_navbar import NavbarViewMixin
from edc_subject_dashboard.view_mixins import SubjectDashboardViewMixin

from ....model_wrappers import AppointmentModelWrapper
from ....model_wrappers import MaternalConsentModelWrapper
from ....model_wrappers import MaternalVisitModelWrapper
from ....model_wrappers import SubjectLocatorModelWrapper


class DashboardView(
        EdcBaseViewMixin, SubjectDashboardViewMixin,
        NavbarViewMixin, BaseDashboardView):

    dashboard_url = 'maternal_subject_dashboard_url'
    dashboard_template = 'maternal_subject_dashboard_template'
    appointment_model = 'edc_appointment.appointment'
    appointment_model_wrapper_cls = AppointmentModelWrapper
    consent_model = 'td_maternal.maternalconsent'
    consent_model_wrapper_cls = MaternalConsentModelWrapper
    navbar_name = 'td_dashboard'
    navbar_selected_item = 'consented_subject'
    subject_locator_model = 'edc_locator.subjectlocator'
    subject_locator_model_wrapper_cls = SubjectLocatorModelWrapper
    visit_model_wrapper_cls = MaternalVisitModelWrapper
