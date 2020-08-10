import hashlib
import re
import json
import requests
from django.conf import settings

# settings.configure(DEBUG=True)

MAILCHIMP_API_KEY           = getattr(settings, "MAILCHIMP_API_KEY", None)
MAILCHIMP_DATA_CENTER       = getattr(settings, "MAILCHIMP_DATA_CENTER", None)
MAILCHIMP_EMAIL_LIST_ID     = getattr(settings, "MAILCHIMP_EMAIL_LIST_ID", None)


def check_email(email):
    if not re.match(r".+@.+\..+", email):
        raise ValueError("String passed is not a valid email format")
    return email


def get_subscriber_hash(member_email):
    # check email.  Hashed required by mailchipm as its on the url
    check_email(member_email)
    member_email = member_email.lower().encode()
    hashed_email = hashlib.md5(member_email)
    return hashed_email.hexdigest()

class Mailchimp(object):
    def __init__(self):
        super(Mailchimp, self).__init__()
        self.key = MAILCHIMP_API_KEY
        # base url + endpoint added later in other defs
        self.api_url = "https://{dc}.api.mailchimp.com/3.0".format(dc=MAILCHIMP_DATA_CENTER)
        self.list_id = MAILCHIMP_EMAIL_LIST_ID
        self.list_endpoint = '{api_url}/lists/{list_id}'.format(
                                    api_url = self.api_url,
                                    list_id=self.list_id
                        )

    def get_members_endpoint(self):
        return self.list_endpoint + "/members"

    def change_subscription_status(self, email, status="unsubscribed"):
        # endpoint -> get the api location
        # method -> the post/get
        # data -> data being passed
        # auth -> authentication
        # important to use hash as its on the URL vs post which is on https
        hashed_email = get_subscriber_hash(email)
        endpoint = self.get_members_endpoint() + "/" + hashed_email
        data = {
            "email_address": email,
            "status": self.check_valid_status(status)
        }
        r = requests.put(endpoint, auth=("", self.key), data=json.dumps(data))
        return r.status_code, r.json()

    def check_subscription_status(self, email):
        # endpoint -> get the api location
        # method -> the post/get
        # data -> data being passed
        # auth -> authentication
        # important to use hash as its on the URL vs post which is on https
        hashed_email = get_subscriber_hash(email)
        endpoint = self.get_members_endpoint() + "/" + hashed_email
        r = requests.get(endpoint, auth=("", self.key))
        return r.status_code, r.json()

    def check_valid_status(self, status):
        choices = ["subscribed", "unsubscribed", "cleaned", "pending"]
        if status not in choices:
            raise ValueError("Not a valid choice")
        return status

    def add_email(self, email):
        # endpoint -> get the api location
        # method -> the post/get
        # data -> data being passed
        # auth -> authentication
            # NO LONGER NEEDED - am using change_subscription_status with the hashed email so mailchipm handles this
            # status = "subscribed"
            # self.check_valid_status(status)
            # data = {
            #     "email_address": email,
            #     "status": status
            # }
            # # per https://mailchimp.com/developer/reference/lists/list-members/
            # endpoint = self.get_members_endpoint()
            # r = requests.post(endpoint, auth=("", self.key), data=json.dumps(data))
            # return r.json()
        return self.change_subscription_status(email, status="subscribed")

    def unsubscribe(self, email):
        return self.change_subscription_status(email, status="unsubscribed")

    def subscribe(self, email):
        print(email)
        return self.change_subscription_status(email, status="subscribed")

    def pending(self, email):
        return self.change_subscription_status(email, status="pending")