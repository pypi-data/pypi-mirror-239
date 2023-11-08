from django.views.generic import FormView as DjangoFormView
from kfsd.apps.frontend.views.template import TemplateView
import json

from kfsd.apps.core.utils.dict import DictUtils


class FormView(TemplateView, DjangoFormView):
    def form_invalid(self, form):
        errorsJson = json.loads(form.errors.as_json())
        errors = {}
        for k, v in form.errors.items():
            if k in form.fields:
                oldAttrs = form.fields[k].widget.attrs
                newAttrs = {
                    "class": "form-control is-invalid",
                    "aria-invalid": "true",
                    "aria-describedby": "{}-error".format(k),
                }
                errors[k] = errorsJson[k][0]["message"]
                form.fields[k].widget.attrs = DictUtils.merge(
                    dict1=oldAttrs, dict2=newAttrs
                )
                form.fields[k].errors = errorsJson[k][0]["message"]

        return self.render_to_response(self.get_context_data(form=form, errors=errors))
