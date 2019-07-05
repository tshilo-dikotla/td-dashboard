from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .antenantal_visit_membership_model_wrapper import AntenatalVisitMembershipModelWrapper


class AntenatalVisitMembershipWrapperMixin:

    anv_model_wrapper_cls = AntenatalVisitMembershipModelWrapper

    @property
    def antenatal_visit_membership_cls(self):
        return django_apps.get_model('td_maternal.antenatalvisitmembership')

    @property
    def antenatal_visit_membership_model_obj(self):
        """Returns a Antenatal Visit Membership model instance or None.
        """
        try:
            return self.antenatal_visit_membership_cls.objects.get(
                **self.antenatal_visit_membership_options)
        except ObjectDoesNotExist:
            return None

    @property
    def antenatal_visit_membership(self):
        """Returns a wrapped saved or unsaved antenatal visit membership.
        """
        model_obj = (
            self.antenatal_visit_membership_model_obj or
            self.antenatal_visit_membership_cls(
                **self.create_antenatal_visit_membership_options))
        return self.anv_model_wrapper_cls(
            model_obj=model_obj)

    @property
    def create_antenatal_visit_membership_options(self):
        """Returns a dictionary of options to create a new
        unpersisted antenatal visit membership model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def antenatal_visit_membership_options(self):
        """Returns a dictionary of options to get an existing
        antenatal visit membership model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options
