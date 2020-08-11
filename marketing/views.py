from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import UpdateView

# Create your views here.

from .forms import MarketingPreferenceForm
from .models import MarketingPreference

class MarketingPreferenceUpdateView(SuccessMessageMixin, UpdateView):
    form_class = MarketingPreferenceForm
    template_name = "base/forms.html"   # need to create
    # override default absolute url (below).  No get url method anyways on the model
    success_url = "/settings/email/"
    success_message = "Your email preferences have been updated to Mailchimp"

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect("/login/?next=/settings/email/")     # HttpResponse("<h1>Not allowed</h1>", status=400)
        return super(MarketingPreferenceUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(MarketingPreferenceUpdateView, self).get_context_data(*args, **kwargs)
        context["title"] = "Update Marketing Preferences"
        return context

    def get_object(self):
        user = self.request.user
        obj, created = MarketingPreference.objects.get_or_create(user=user) # get abs url
        return obj

