from kfsd.apps.frontend.views.base import BaseTemplate


class Custom404View(BaseTemplate):
    template_name = "v1/errors/404.html"
