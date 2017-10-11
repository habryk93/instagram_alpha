from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404
from django.urls import reverse
from django.views.generic import ListView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from dashboard.forms import PictureForm
from dashboard.models import Picture
from django.conf import settings


class DashboardView(ListView):
    model = Picture
    template_name = "dashboard.html"
    context_object_name = 'pictures'
    paginate_by = 12


class PictureDetailView(DetailView):
    model = Picture

    def get_context_data(self, **kwargs):
        context = super(PictureDetailView, self).get_context_data(**kwargs)
        context['google_map_api_key'] = settings.GOOGLE_MAPS_API_KEY
        return context


class PictureAddView(LoginRequiredMixin, CreateView):
    template_name = 'picture/add.html'
    form_class = PictureForm

    def get_login_url(self):
        return reverse('instagram.login')

    def get_success_url(self):
        return reverse('picture_info', args=(self.object.slug,))

    def form_valid(self, form):
        picture = form.save()
        picture.user = self.request.user
        picture.save()

        return super(PictureAddView, self).form_valid(form)


class PictureDeleteView(LoginRequiredMixin, DeleteView):
    model = Picture

    def get_success_url(self):
        return reverse('dashboard')

    def get_object(self, queryset=None):
        obj = super(PictureDeleteView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj