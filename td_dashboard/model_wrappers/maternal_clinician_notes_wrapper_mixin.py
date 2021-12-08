from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .maternal_clinician_notes_model_wrapper import MaternalClinicianNotesModelWrapper


class MaternalClinicianNotesModelWrapperMixin:

    maternal_clinician_notes_model_wrapper_cls = MaternalClinicianNotesModelWrapper

    @property
    def maternal_clinician_notes_model_obj(self):
        """Returns a maternal clinician notes model instance or None.
        """
        try:
            return self.maternal_clinician_notes_cls.objects.get(
                **self.maternal_clinician_notes_options)
        except ObjectDoesNotExist:
            return None

    @property
    def maternal_clinician_notes(self):
        """Returns a wrapped saved or unsaved maternal clinician notes.
        """
        model_obj = self.maternal_clinician_notes_model_obj or self.maternal_clinician_notes_cls(
            **self.create_maternal_clinician_notes_options)
        return self.maternal_clinician_notes_model_wrapper_cls(model_obj=model_obj)

    @property
    def maternal_clinician_notes_cls(self):
        return django_apps.get_model('td_maternal.cliniciannotesarchives')

    @property
    def create_maternal_clinician_notes_options(self):
        """Returns a dictionary of options to create a new
        unpersisted maternal clinician notes model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def maternal_clinician_notes_options(self):
        """Returns a dictionary of options to get an existing
        maternal clinician notes model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options
