from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .subject_locator_model_wrapper import SubjectLocatorModelWrapper


class MaternalLocatorModelWrapperMixin:

    maternal_locator_model_wrapper_cls = SubjectLocatorModelWrapper

    @property
    def maternal_locator_model_obj(self):
        """Returns a subject locator model instance or None.
        """
        try:
            return self.maternal_locator_cls.objects.get(**self.maternal_locator_options)
        except ObjectDoesNotExist:
            return None

    @property
    def maternal_locator(self):
        """Returns a wrapped saved or unsaved maternal locator.
        """
        model_obj = self.maternal_locator_model_obj or self.maternal_locator_cls(
            **self.create_maternal_locator_options)
        return self.maternal_locator_model_wrapper_cls(model_obj=model_obj)

    @property
    def maternal_locator_cls(self):
        return django_apps.get_model('td_maternal.maternallocator')

    @property
    def create_maternal_locator_options(self):
        """Returns a dictionary of options to create a new
        unpersisted maternal locator model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def maternal_locator_options(self):
        """Returns a dictionary of options to get an existing
        maternal locator instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options
