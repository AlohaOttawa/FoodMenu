from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView
from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse

from django.utils.http import is_safe_url
from .models import GuestEmail
from .forms import LoginForm, RegisterForm, GuestForm

# Create your views here.

def guest_register_view(request):
    form = GuestForm(request.POST or None)
    context = {
        "form": form
    }
        # print("User is logged in? " + str(request.user.is_authenticated))

    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email   = form.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session["guest_email_id"] = new_guest_email.id

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("/register/")
    return redirect("/register/")


class LoginView(FormView):
    form_class = LoginForm
    success_url = "/"
    template_name = "accounts/login.html"

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get("next")
        next_post = request.POST.get("next")
        redirect_path = next_ or next_post or None

        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            try:
                del request.session["guest_email_id"]
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        return super(LoginView, self).form_invalid(form)


            # LoginView above replaces the login page below (same as register)

            # def login_page(request):
            #     form = LoginForm(request.POST or None)
            #     context = {
            #         "form": form
            #     }
            #         # print("User is logged in? " + str(request.user.is_authenticated))
            #
            #     next_ = request.GET.get("next")
            #     next_post = request.POST.get("next")
            #     redirect_path = next_ or next_post or None
            #     if form.is_valid():
            #             # print(form.cleaned_data)
            #         username = form.cleaned_data.get("username")
            #         password = form.cleaned_data.get("password")
            #         user = authenticate(request, username=username, password=password)
            #         if user is not None:
            #             login(request, user)
            #             try:
            #                 del request.session["guest_email_id"]
            #             except:
            #                 pass
            #             if is_safe_url(redirect_path, request.get_host()):
            #                 return redirect(redirect_path)
            #             else:
            #                 return redirect("/")
            #             # print(request.user.is_authenticated)
            #             # Redirect to a success page.
            #         else:
            #             # Return an 'invalid login' error message
            #             print("Error in login credentials")
            #
            #     return render(request, "accounts/login.html", context)

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = "/login/"


            # MOving code below out to replace by class RegisterView(CreateView) above to classify from def
            # to a class based view

            # User = get_user_model()
            # def register_page(request):
            #     form = RegisterForm(request.POST or None)
            #     context = {
            #         "form": form
            #     }
            #     if form.is_valid():
            #         form.save()
            #                 # -- No longer needed.  Using Custom model manager in accounts.  Added form.save() above instead
            #                 # print(form.cleaned_data)
            #                 # username = form.cleaned_data.get("username")
            #                 # password = form.cleaned_data.get("password")
            #                 # email = form.cleaned_data.get("email")
            #                 # new_user = User.objects.create_user(username, email, password)
            #                 # print(new_user)
            #     return render(request, "accounts/register.html", context)