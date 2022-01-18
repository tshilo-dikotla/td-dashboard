from django.conf import settings
from edc_model_wrapper import ModelWrapper
from edc_odk.model_wrappers import OmangCopiesModelWrapperMixin
from edc_odk.model_wrappers import NoteToFileModelWrapperMixin
from edc_odk.model_wrappers import SpecimenConsentModelWrapperMixin as ODKSpecimenConsentModelWrapperMixin
from edc_odk.model_wrappers import ConsentCopiesModelWrapperMixin
from edc_odk.model_wrappers import ClinicianNotesModelWrapperMixin
from edc_odk.model_wrappers import LabResultsModelWrapperMixin

from .td_consent_version_model_wrapper_mixin import TDConsentVersionModelWrapperMixin


class SubjectConsentModelWrapper(ClinicianNotesModelWrapperMixin,
                                 LabResultsModelWrapperMixin,
                                 ODKSpecimenConsentModelWrapperMixin,
                                 OmangCopiesModelWrapperMixin,
                                 ConsentCopiesModelWrapperMixin,
                                 NoteToFileModelWrapperMixin,
                                 TDConsentVersionModelWrapperMixin,
                                 ModelWrapper):

    model = 'td_maternal.subjectconsent'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'screening_listboard_url')
    next_url_attrs = ['screening_identifier']
    querystring_attrs = ['screening_identifier', 'subject_identifier']
