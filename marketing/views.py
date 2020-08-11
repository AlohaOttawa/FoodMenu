from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import UpdateView, View
from django.conf import settings

# Create your views here.

from .forms import MarketingPreferenceForm
from .mixins import CsrfExemptMixin
from .models import MarketingPreference
from .utils import Mailchimp

MAILCHIMP_EMAIL_LIST_ID     = getattr(settings, "MAILCHIMP_EMAIL_LIST_ID", None)

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


"""
POST METHOD
data[email]:
crv19@gmail.com
data[email_type]:
html
Copy Path
•
Copy Value
data[id]:
534cac8862
data[ip_opt]:
198.8.85.48
data[list_id]:
f0f91d25e7
data[merges][ADDRESS]:
data[merges][BIRTHDAY]:
data[merges][EMAIL]:
crv19@gmail.com
data[merges][FNAME]:
data[merges][LNAME]:
data[merges][PHONE]:
data[web_id]:
164527842
fired_at:
2020-08-11 21:22:38
type:
subscribe
"""

class MailchimpWebhookView(CsrfExemptMixin, View): # identical.  HTTP GET method -- def get()
    def get(self, request, *args, **kwargs):
        return HttpResponse("<h1>Test mailchimp - thank you</h1>", status=200)


    def post(self, request, *args, **kwargs):
        data = request.POST  # usually a dictionary with key value pairs
        list_id = data.get("data[list_id]")
        if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
            email = data.get("data[email]")
            hook_type = data.get("type")
            response_status, response = Mailchimp().check_subscription_status(email)
            subcription_status = response["status"]

            is_sub = None
            mailchimp_sub = None

            if subcription_status == "subscribed":
                is_sub, mailchimp_sub = (True, True)

            elif subcription_status == "unsubscribed":
                is_sub, mailchimp_sub = (False, False)

            if is_sub is not None and mailchimp_sub is not None:
                qs = MarketingPreference.objects.filter(user_email_iexact=email)
                if qs.exists():
                    qs.update(subscribed=is_sub,
                              mailchimp_subscribed=mailchimp_sub,
                              mailchimp_msg=str(data))

        return HttpResponse("THanks!", status=200)


def mailchimp_webhook_view(request):
    data = request.POST # usually a dictionary with key value pairs
    list_id = data.get("data[list_id]")
    if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
        email = data.get("data[email]")
        hook_type = data.get("type")
        response_status, response = Mailchimp().check_subscription_status(email)
        subcription_status = response["status"]

        is_sub = None
        mailchimp_sub = None

        if subcription_status == "subscribed":
            is_sub, mailchimp_sub = (True, True)

        elif subcription_status == "unsubscribed":
            is_sub, mailchimp_sub = (False, False)

        if is_sub is not None and mailchimp_sub is not None:
            qs = MarketingPreference.objects.filter(user_email_iexact=email)
            if qs.exists():
                qs.update(subscribed=is_sub,
                          mailchimp_subscribed=mailchimp_sub,
                          mailchimp_msg=str(data))


    return HttpResponse("THanks!", status=200)