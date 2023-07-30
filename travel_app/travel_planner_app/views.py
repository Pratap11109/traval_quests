from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from .models import BudgetPlanner, Review
from .forms import ReviewForm


def index(request):
    # Add view for the homepage
    return render(request, "index.html")


def login_view(request):
    # Add view for the login page
    return render(request, "login.html")


# def signup(request):
#     # Add view for the signup page
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         new_user = ExternalUser(username=username, email=email)
#         new_user.set_password(password)
#         new_user.save()
#         return redirect('index')
#     return render(request, 'signup.html')


def main_page(request):
    if request.method == "POST":
        start_date = request.POST.get("start-date")
        end_date = request.POST.get("end-date")
        num_days = request.POST.get("num-days")
        theme = request.POST.get("theme")
        budget = request.POST.get("budget")
        budget_plan = {
            "budget": budget,
            "theme": theme,
            "num_days": num_days,
            "end_date": end_date,
            "start_date": start_date
        }

        budget_plan = BudgetPlanner(**budget_plan)
        budget_plan.save()
        return  render(request, "feedback.html")
        # Do something with the form data (e.g., save to database, perform some action)
        # ...

        # Return a response after processing the form data

    # If the request method is not POST, render the form template again
    return render(request, "main.html")


def signup(request):
    form = UserRegistrationForm
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name="Customer")
            user.groups.add(group)

            username = form.cleaned_data.get("username")
            messages.success(request, "New account created:" + username)
            return redirect("login")
        else:
            messages.error(request, "not register")
    return render(request, "signup.html", {"form": form})


@login_required(login_url="login")
def input_page(request):
    # Add view for the input page
    return render(request, "main.html")


def feedback(request):
    # Add view for the input page
    if request.method == "POST":
        print("Inside post")
        name_of_place = request.POST.get("name_of_place")
        print(name_of_place)
        date_of_visit = request.POST.get("date")
        rating = request.POST.get("rating")
        liked_most = request.POST.getlist("likedMost")  # Get list of selected options
        disliked_most = request.POST.getlist("dislikedMost")  # Get list of selected options
        overall_experience = request.POST.get("overallExperience")

        # Save the data to the Review model or perform other actions as needed
        review = Review(
            name_of_place=name_of_place,
            date_of_visit=date_of_visit,
            rating=rating,
            liked_most=", ".join(liked_most),
            disliked_most=", ".join(disliked_most),
            overall_experience=overall_experience,
        )
        review.save()

        # Redirect to a success page or do something else
        return redirect("main_page")

    return render(request, "feedback.html")
    # return render(request, 'feedback.html')

@login_required(login_url="login")
def output_page(request):
    # Add view for the output page
    return HttpResponse("output page")


@login_required(login_url="login")
def automated_plan(request):
    # Add view for the automated travel plan
    return HttpResponse("automated-plan")


@login_required(login_url="login")
def customized_plan(request):
    # Add view for the customized travel plan
    return HttpResponse("customized-plan")


@login_required(login_url="login")
def trip_with_strangers(request):
    if request.method == "POST":
        # Process the form submission and handle user requests to join the travel group
        # You can use forms or AJAX requests to handle this functionality
        # For simplicity, we'll assume the form has a checkbox for activating the option

        # Sample code (not complete):
        if "join_group" in request.POST:
            # Handle user's request to join the group
            # Get the travel group from the database based on the user's selection
            selected_group_id = request.POST.get("group_id")
            travel_group = TravelGroup.objects.get(pk=selected_group_id)
            travel_group.members.add(
                request.user
            )  # Add the user to the group's members

    # Get the user's owned and joined travel groups
    owned_groups = TravelGroup.objects.filter(owner=request.user)
    joined_groups = TravelGroup.objects.filter(members=request.user)

    context = {
        "owned_groups": owned_groups,
        "joined_groups": joined_groups,
    }
    return render(request, "trip_with_strangers.html", context)
