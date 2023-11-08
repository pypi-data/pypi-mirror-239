from kfsd.apps.frontend.views.template import TemplateView


class BaseTemplate(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["social"] = {
            "github": "https://github.com/kubefacets",
            "twitter": "https://twitter.com/kubefacets",
            "youtube": "https://www.youtube.com/@Kubefacets",
            "company_name": "Kubefacets, Inc",
            "website": "kubefacets.com",
            "home_pg": "https://kubefacets.com",
        }
        return context
