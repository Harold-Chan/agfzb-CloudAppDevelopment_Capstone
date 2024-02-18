from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from urllib.parse import quote_plus
from .restapis import get_dealers_from_cf
from .restapis import get_dealer_by_id_from_cf
from .restapis import get_dealer_reviews_from_cf


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    if request.method == "GET":
        return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to index again
            messages.error(request, 'Incorrect username or password')
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user '{}'".format(request.user.username))
    #Logout user in the request
    logout(request)
    # Redirect user back to index page
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        password = request.POST['psw']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect('djangoapp:index')
        else:
            messages.error(request, 'Username already exists')
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://cchharold-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        context['content'] = dealer_names
        # Render index.html with context
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, id):
    if request.method == "GET":
        context = {}
        dealer_url = "https://cchharold-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
        context["dealer"] = dealer
    
        encoded_id = quote_plus(str(id))
        review_url = f"https://cchharold-5000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews?id={encoded_id}"
        reviews = get_dealer_reviews_from_cf(review_url, id=id)
        print(reviews)
        context["reviews"] = reviews
        
        # Construct a dictionary with detailed dealer and reviews information
        response_data = {
            "dealer": {
                "id": dealer.id,
                "full_name": dealer.full_name,
                "address": dealer.address,
                "city": dealer.city,
                "st": dealer.st,
                "zip": dealer.zip,
                "lat": dealer.lat,
                "long": dealer.long
            },
            "reviews": [
                {
                    "reviewer": review.reviewer,
                    "purchase": review.purchase,
                    "review": review.review,
                    "purchase_date": review.purchase_date.strftime('%Y-%m-%d'),
                    "car_make": review.car_make,
                    "car_model": review.car_model,
                    "car_year": review.car_year,
                    "sentiment": review.sentiment
                }
                for review in reviews
            ]
        }

        # Convert the dictionary to a JSON string
        response_json = json.dumps(response_data, cls=DjangoJSONEncoder)

        # Return the JSON string as an HttpResponse
        return HttpResponse(response_json, content_type='application/json')
        #return render(request, 'djangoapp/dealer_details.html', context)



# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

