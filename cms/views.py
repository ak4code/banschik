from django.views.generic import TemplateView, DetailView
from .models import Settings, Page


class HomePage(TemplateView):
    template_name = 'cms/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['settings'] = Settings.get_solo()
        except:
            context['settings'] = []
            print('No init base settings')
        return context


class PageView(DetailView):
    model = Page
