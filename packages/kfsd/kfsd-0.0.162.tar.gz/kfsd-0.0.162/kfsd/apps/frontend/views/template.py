from django.views.generic import TemplateView as DjangoTemplateView
from kfsd.apps.core.utils.dict import DictUtils


class BaseTemplate(DjangoTemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fileHost = DictUtils.get_by_path(self.request.config, "services.file_api.host")
        context["STATIC_URL"] = fileHost
        context["social"] = {
            "github": "https://github.com/kubefacets",
            "twitter": "https://twitter.com/kubefacets",
            "youtube": "https://www.youtube.com/@Kubefacets",
            "company_name": "Kubefacets, Inc",
            "website": "kubefacets.com",
            "home_pg": "https://kubefacets.com",
        }
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["user"] = self.request.token_user
        return self.render_to_response(context)
