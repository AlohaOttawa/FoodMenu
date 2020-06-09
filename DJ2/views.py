from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import ContactForm, LoginForm, RegisterForm

def new_home_page(request):
    return HttpResponse("<h1>Hello World</h1>")

def home_page(request):
    print(request.session.get("first_name", "Unknown"))     # GEts the value from carts/templates/views
    # request.session["first name"}

    context = {
        "title": "CRV19 - food comfort in the covid era!",
        "content":"Welcome to the Home Page"
    }

    if request.user.is_authenticated:
        context["premium"] = "Premium logged in content for Mom and Max"
    return render(request, "home_page.html", context)

def about_page(request):
    context = {
        "title": "About Page",
        "content":"Welcome to the About Page"
    }
    return render(request, "home_page.html", context)

def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title": "Contact Page",
        "content":"Welcome to the Contact page",
        "form": contact_form
    }

    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    # if request.method == "POST":
    #     print(request.POST)
    #     print(request.POST.get("fullname"))
    #     print(request.POST.get("email"))
    #     print(request.POST.get("content"))
    #     print(request.POST.get("csrfmiddlewaretoken"))
    return render(request, "contact/view.html", context)

def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    print("User is logged in? " + str(request.user.is_authenticated))
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(request.user.is_authenticated)
            # Redirect to a success page.
            # context['form'] = LoginForm()   << hal - old code >>
            return redirect("/")
        else:
            # Return an 'invalid login' error message
            print("Error in login credentials")


    return render(request, "auth/login.html", context)

User = get_user_model()
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        new_user = User.objects.create_user(username, email, password)
        print(new_user)
    return render(request, "auth/register.html", context)