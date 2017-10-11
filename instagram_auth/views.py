# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.views.generic import FormView


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse('instagram.login')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        authenticate(username=username, password=raw_password)

        return super(RegisterView, self).form_valid(form)
