from kfsd.apps.frontend.views.base import BaseTemplate


class Custom403View(BaseTemplate):
    template_name = "v1/errors/403.html"
