from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .maternal_contact_model_wrapper import MaternalContactModelWrapper


class MaternalContactModelWrapperMixin:

    maternal_contact_model_wrapper_cls = MaternalContactModelWrapper

    @property
    def maternal_contact_model_obj(self):
        """Returns a maternal contact model instance or None.
        """
        try:
            return self.maternal_contact_cls.objects.get(**self.maternal_contact_options)
        except ObjectDoesNotExist:
            return None

    @property
    def maternal_contact(self):
        """Returns a wrapped unsaved maternal contact.
        """
        model_obj = self.maternal_contact_cls(
            **self.create_maternal_contact_options)
        return self.maternal_contact_model_wrapper_cls(model_obj=model_obj)

    @property
    def maternal_contact_cls(self):
        return django_apps.get_model('td_maternal.maternalcontact')

    @property
    def create_maternal_contact_options(self):
        """Returns a dictionary of options to create a new
        unpersisted maternal contact model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def maternal_contact_options(self):
        """Returns a dictionary of options to get an existing
        maternal contact model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options
