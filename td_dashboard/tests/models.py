from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_mixins import BaseUuidModel


class Appointment(BaseUuidModel):

    visit_code = models.CharField(
        max_length=25,
        null=True,
        editable=False)

    appt_datetime = models.DateTimeField(
        verbose_name=('Appointment date and time'),
        db_index=True)

    subject_identifier = models.CharField(max_length=25)


class SubjectVisit(BaseUuidModel):

    appointment = models.OneToOneField(Appointment, on_delete=PROTECT)

    subject_identifier = models.CharField(max_length=25)

    visit_code = models.CharField(
        max_length=25,
        null=True,
        editable=False)


class SubjectConsent(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    screening_identifier = models.CharField(max_length=25)

    gender = models.CharField(max_length=25, default='M')

    initials = models.CharField(max_length=25, default='XX')

    first_name = models.CharField(max_length=25, default='NOAM')
