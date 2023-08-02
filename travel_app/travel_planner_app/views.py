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
from langchain.llms import OpenAI


def index(request):
    # Add view for the homepage
    return render(request, "index.html")


def login_view(request):
    # Add view for the login page
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                # Redirect to the home page or any other page after successful login
                return redirect("main_page")
            else:
                return redirect("login")
    else:
        form = AuthenticationForm()
    return render(request, "login.html")




def main_page(request):
    start_date, end_date, num_days, theme, current_location, budget = None, None, None, None, None, None

    if request.method == "POST":
        start_date = request.POST.get("start-date")
        end_date = request.POST.get("end-date")
        num_days = request.POST.get("num-days")
        theme = request.POST.get("theme")
        current_location = request.POST.get(current_location)
        budget = request.POST.get("budget")

        budget_plan = {
            "budget": budget,
            "theme": theme,
            "current_location": current_location,
            "num_days": num_days,
            "end_date": end_date,
            "start_date": start_date
        }
        start_point = current_location
        budget_plan = BudgetPlanner(**budget_plan)
        budget_plan.save()
        llm = OpenAI(temperature=0.6, openai_api_key="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")
       
        stri = llm( "Can you suggest a top 2 traveling plan for me? I'll be starting on {0} and ending on {1}. The trip will be for {2} days, and my budget is {3}rs, starting point is {4} give me list of destinations, only place name".format(start_date, end_date,num_days, budget, start_point))
        print(stri)
        print("===========================================================================")
        destinations_list = [destination.strip() for destination in stri.split('\n')]
        print(destinations_list)
        print("8888888888888888888888888888888888888888888888888888888888888888888888888")
        result_list = []
        for destination in destinations_list:
            if (not destination) or destination == "":
                continue
            days_formate = """I'll be starting on {0} and ending on {1}. The trip will be for {2} days, and my budget is {3}, starting from {4} and the destination is {5}. Please include transportation options and a complete itinerary with paths to go to each destination give me in dict formate all details""".format(start_date, end_date,num_days,budget, start_point, destination)
            result = llm(days_formate)
            print(result)
            print("*"*10)
            result_list.append({destination: result})
        print(result_list)
        return  render(request, "output.html", {"result_list": result_list})
        # Do something with the form data (e.g., save to database, perform some action)
        # ...

        # Return a response after processing the form data

    # If the request method is not POST, render the form template again
    return render(request, "main.html")


def signup(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user registration data to the UserSignup model

            username = form.cleaned_data.get("username")
            messages.success(request, "New account created: " + username)
            return redirect("login")
        else:
            messages.error(request, "Not registered")
    return render(request, "signup.html", {"form": form})


# @login_required(login_url="login")
def input_page(request):
    # Add view for the input page
    return render(request, "main.html")

# @login_required(login_url="login")
def feedback(request):
    # Add view for the input page
    if request.method == "POST":
        name_of_place = request.POST.get("name_of_place")
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
        return render(request, "main.html")

    return render(request, "feedback.html")

# @login_required(login_url="login")
def output_page(request):
    # Add view for the output page
    return HttpResponse("output page")


# @login_required(login_url="login")
def automated_plan(request):
    # Add view for the automated travel plan
    return HttpResponse("automated-plan")


# @login_required(login_url="login")
def customized_plan(request):
    # Add view for the customized travel plan
    return HttpResponse("customized-plan")


# @login_required(login_url="login")
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


def output(request):
    

    llm = OpenAI(temperature=0.6, openai_api_key="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")

    start_date = "12-08-2023"
    end_date = "12-08-2023"
    days = "4"
    budget = "5000"
    start_point = "Pune"
    # chat_model = ChatOpenAI()
    stri = llm( "Can you suggest a top 10 traveling plan for me? I'll be starting on {0} and ending on {1}. The trip will be for {2} days, and my budget is {3}rs, starting point is {4} give me list of destinations, only place name".format(start_date, end_date,days,budget, start_point))
            
    destinations_list = [destination.strip() for destination in stri.split('\n')]
    result_list = []
    for destination in destinations_list:
        days_formate = """I'll be starting on {0} and ending on {1}. The trip will be for {2} days, and my budget is {3}, starting from {4} and the destination is {5}. Please include transportation options and a complete itinerary with paths to go to each destination give me in dict formate all details""".format(start_date, end_date,days,budget, start_point, destination)
        result = llm(days_formate)


        ans = {"day": []}

        for key, value in result.items():
            if "Day" in key:
                ans["day"].append({key: value})
            else:
                ans[key] = value


        result_list.append(ans)
    
    context = {
        "result": result_list
    }

    print(result)
    render(request, "trip_with_strangers.html", context)


