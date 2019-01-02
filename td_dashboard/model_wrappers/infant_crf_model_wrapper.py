from edc_visit_schedule.model_wrappers import (
    CrfModelWrapper as BaseCrfModelWrapper)


class InfantCrfModelWrapper(BaseCrfModelWrapper):

    visit_model_attr = 'infant_visit'

    querystring_attrs = [visit_model_attr]

    @property
    def infant_visit(self):
        return str(getattr(self.object, self.visit_model_attr).id)
