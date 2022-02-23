from django.views.generic import TemplateView


class TestView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test'] = 'okok'

        return context

    def get(self, request, *args, **kwargs):
        print(request.user.session_set.all())

        return super().get(request, *args, **kwargs)

