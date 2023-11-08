from kfsd.apps.frontend.views.base import BaseTemplate


class Custom500View(BaseTemplate):
    template_name = "v1/errors/500.html"
