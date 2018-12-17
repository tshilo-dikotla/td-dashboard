from edc_visit_schedule.model_wrappers import CrfModelWrapper as BaseCrfModelWrapper


class CrfModelWrapper(BaseCrfModelWrapper):

    visit_model_attr = 'maternal_visit'

    @property
    def maternal_visit(self):
        return str(getattr(self.object, self.visit_model_attr).id)
