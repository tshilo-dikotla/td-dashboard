from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .maternal_offstudy_model_wrapper import MaternalOffstudyModelWrapper


class MaternalOffstudyModelWrapperMixin:

    maternal_offstudy_model_wrapper_cls = MaternalOffstudyModelWrapper

    @property
    def maternal_offstudy_model_obj(self):
        """Returns a maternal offstudy model instance or None.
        """
        try:
            return self.maternal_offstudy_cls.objects.get(**self.maternal_offstudy_options)
        except ObjectDoesNotExist:
            return None

    @property
    def maternal_offstudy(self):
        """Returns a wrapped saved or unsaved maternal offstudy.
        """
        model_obj = self.maternal_offstudy_model_obj or self.maternal_offstudy_cls(
            **self.create_maternal_offstudy_options)
        return self.maternal_offstudy_model_wrapper_cls(model_obj=model_obj)

    @property
    def maternal_offstudy_cls(self):
        return django_apps.get_model('td_maternal.maternaloffstudy')

    @property
    def create_maternal_offstudy_options(self):
        """Returns a dictionary of options to create a new
        unpersisted maternal offstudy model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def maternal_offstudy_options(self):
        """Returns a dictionary of options to get an existing
        maternal offstudy model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options
