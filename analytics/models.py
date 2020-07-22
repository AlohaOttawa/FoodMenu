from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from .signals import object_viewed_signal
from .utils import get_client_ip
from accounts.signals import user_logged_in

# Create your models here.

User = settings.AUTH_USER_MODEL

FORCE_SESSION_TO_ONE = getattr(settings, "FORCE_SESSION_TO_ONE", False)
FORCE_INACTIVE_USER_ENDSESSION = getattr(settings, "FORCE_INACTIVE_USER_ENDSESSION", False)

class ObjectViewed(models.Model):
    user            = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL) # user instance
    ip_address      = models.CharField(max_length=250, blank=True, null=True) # not use Django
    # the 3 below encapsulates the core model objects
    content_type    = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING) # all models MenuItem, Order, cart, etc.
    object_id       = models.PositiveIntegerField() # menuitem.id, order.id, etc.
    content_object  = GenericForeignKey("content_type", "object_id") # menuitem instance, etc.
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s viewed on %s"%(self.content_object, self.timestamp)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Object viewed"
        verbose_name_plural = "Objects viewed"


    # instance and request per signals.py def signal with 'instance', 'request' parms
def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    con_type = ContentType.objects.get_for_model(sender)    # same as instance.__class__
    user_session_key = request.session.session_key
    try:
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None
    except:
        pass

    new_view_obj = ObjectViewed.objects.create(
        user = user,
        content_type = con_type,
        object_id = instance.id,
        ip_address = get_client_ip(request)
    )


    # sender is sent along with signal itself as instance
object_viewed_signal.connect(object_viewed_receiver)



class UserSession(models.Model):
    user            = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL) # user instance
    ip_address      = models.CharField(max_length=250, blank=True, null=True) # not use Django
    session_key     = models.CharField(max_length=100, null=True, blank=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    active          = models.BooleanField(default=True)
    ended           = models.BooleanField(default=False)

    def __str__(self):
        return self.session_key

    def end_session(self):
        session_key = self.session_key
        ended = self.ended
        try:
            Session.objects.get(pk=session_key).delete()
            self.active = False
            self.ended = True
            self.save()
        except:
            pass
        return self.ended

def post_save_session_receiver(sender, instance, created, *args, **kwargs):
    if created:
        qs = UserSession.objects.filter(user=instance.user, ended=False, active=False).exclude(id = instance.id)
        for i in qs:
            i.end_session()
        # if not acctive but the session is still alive, kill the session
    if not instance.active and not instance.ended:
        instance.end_session()

if FORCE_SESSION_TO_ONE:
    post_save.connect(post_save_session_receiver, sender=UserSession)

        # failsafe below not required

def post_save_user_changed_receiver(sender, instance, created, *args, **kwargs):
    if not created:
        if instance.is_active == False:
            qs = UserSession.objects.filter(user=instance.user, ended=False, active=False)
            for i in qs:
                i.end_session()

if FORCE_INACTIVE_USER_ENDSESSION:
    post_save.connect(post_save_user_changed_receiver, sender=User)


def user_logged_in_receiver(sender, instance, request, *args, **kwargs):
    # print(instance)
    user = instance
    ip_address = get_client_ip(request)
    session_key = request.session.session_key
    UserSession.objects.create(
        user=user,
        ip_address=ip_address,
        session_key=session_key
    )


user_logged_in.connect(user_logged_in_receiver)