from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .maternal_labour_del_model_wrapper import MaternalLabourDelModelWrapper


class MaternalLabourDelModelWrapperMixin:

    maternal_labour_del_model_wrapper_cls = MaternalLabourDelModelWrapper

    @property
    def maternal_labour_del_model_obj(self):
        """Returns a maternal labor del model instance or None.
        """
        try:
            return self.maternal_labour_del_cls.objects.get(**self.maternal_labour_del_options)
        except ObjectDoesNotExist:
            return None

    @property
    def maternal_labour_del(self):
        """Returns a wrapped saved or unsaved maternal labor del.
        """
        model_obj = self.maternal_labour_del_model_obj or self.maternal_labour_del_cls(
            **self.create_maternal_labour_del_options)
        return self.maternal_labour_del_model_wrapper_cls(model_obj=model_obj)

    @property
    def maternal_labour_del_cls(self):
        return django_apps.get_model('td_maternal.maternallabourdel')

    @property
    def create_maternal_labour_del_options(self):
        """Returns a dictionary of options to create a new
        unpersisted maternal labor del model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def maternal_labour_del_options(self):
        """Returns a dictionary of options to get an existing
        maternal labor del model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def maternal_ultrasound_initial_obj(self):
        ultrasound_initial_cls = django_apps.get_model(
            'td_maternal.maternalultrasoundinitial')
        try:
            return ultrasound_initial_cls.objects.get(
                maternal_visit__subject_identifier=self.object.subject_identifier)
        except ObjectDoesNotExist:
            return None
