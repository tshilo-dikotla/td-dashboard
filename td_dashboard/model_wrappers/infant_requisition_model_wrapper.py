from edc_visit_schedule.model_wrappers import RequisitionModelWrapper


class InfantRequisitionModelWrapper(RequisitionModelWrapper):

    visit_model_attr = 'infant_visit'

    querystring_attrs = [visit_model_attr, 'panel']

    @property
    def infant_visit(self):
        return str(getattr(self.object, self.visit_model_attr).id)
