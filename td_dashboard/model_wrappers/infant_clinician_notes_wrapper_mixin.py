from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .infant_clinician_notes_model_wrapper import InfantClinicianNotesModelWrapper


class InfantClinicianNotesModelWrapperMixin:

    infant_clinician_notes_model_wrapper_cls = InfantClinicianNotesModelWrapper

    @property
    def infant_clinician_notes_model_obj(self):
        """Returns a infant clinician notes model instance or None.
        """
        try:
            return self.infant_clinician_notes_cls.objects.get(
                **self.infant_clinician_notes_options)
        except ObjectDoesNotExist:
            return None

    @property
    def infant_clinician_notes(self):
        """Returns a wrapped saved or unsaved infant clinician notes.
        """
        model_obj = self.infant_clinician_notes_model_obj or self.infant_clinician_notes_cls(
            **self.create_infant_clinician_notes_options)
        return self.infant_clinician_notes_model_wrapper_cls(model_obj=model_obj)

    @property
    def infant_clinician_notes_cls(self):
        return django_apps.get_model('td_infant.infantcliniciannotesarchives')

    @property
    def create_infant_clinician_notes_options(self):
        """Returns a dictionary of options to create a new
        unpersisted infant clinician notes model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def infant_clinician_notes_options(self):
        """Returns a dictionary of options to get an existing
        infant clinician notes model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options
