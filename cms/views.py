from django.views.generic import TemplateView
from cms.models import Settings


class HomePage(TemplateView):
    template_name = 'cms/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = Settings.get_solo()
        return context
