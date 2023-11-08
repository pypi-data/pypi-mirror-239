from django.views.generic import TemplateView as DjangoTemplateView
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.common.logger import Logger, LogLevel

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class TemplateView(DjangoTemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fileHost = DictUtils.get_by_path(self.request.config, "services.file_api.host")
        context["STATIC_URL"] = fileHost
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["user"] = self.request.token_user
        return self.render_to_response(context)
