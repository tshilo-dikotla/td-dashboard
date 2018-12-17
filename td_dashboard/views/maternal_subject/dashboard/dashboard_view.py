from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.views import DashboardView as BaseDashboardView
from edc_navbar import NavbarViewMixin
from edc_subject_dashboard.view_mixins import SubjectDashboardViewMixin

from ....model_wrappers import (
    AppointmentModelWrapper, SubjectConsentModelWrapper,
    MaternalVisitModelWrapper, SubjectLocatorModelWrapper,
    CrfModelWrapper, RequisitionModelWrapper)


class DashboardView(
        EdcBaseViewMixin, SubjectDashboardViewMixin,
        NavbarViewMixin, BaseDashboardView):

    dashboard_url = 'subject_dashboard_url'
    dashboard_template = 'subject_dashboard_template'
    appointment_model = 'edc_appointment.appointment'
    appointment_model_wrapper_cls = AppointmentModelWrapper
    crf_model_wrapper_cls = CrfModelWrapper
    requisition_model_wrapper_cls = RequisitionModelWrapper
    consent_model = 'td_maternal.subjectconsent'
    consent_model_wrapper_cls = SubjectConsentModelWrapper
    navbar_name = 'td_dashboard'
    visit_attr = 'maternalvisit'
    navbar_selected_item = 'consented_subject'
    subject_locator_model = 'edc_locator.subjectlocator'
    subject_locator_model_wrapper_cls = SubjectLocatorModelWrapper
    visit_model_wrapper_cls = MaternalVisitModelWrapper
